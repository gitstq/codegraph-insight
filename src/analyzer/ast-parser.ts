/**
 * AST 解析器
 */
import { parse } from '@babel/parser';
import traverse from '@babel/traverse';
import * as t from '@babel/types';
import { FileInfo, CodeNode, CodeEdge, NodeType, EdgeType } from '../types';
import { generateId, getRelativePath } from '../utils/file-utils';

/**
 * 解析 JavaScript/TypeScript 文件
 */
export function parseJavaScript(fileInfo: FileInfo, projectRoot: string): { nodes: CodeNode[]; edges: CodeEdge[] } {
  const nodes: CodeNode[] = [];
  const edges: CodeEdge[] = [];
  const relativePath = getRelativePath(fileInfo.path, projectRoot);

  try {
    const ast = parse(fileInfo.content, {
      sourceType: 'module',
      allowImportExportEverywhere: true,
      allowReturnOutsideFunction: true,
      plugins: [
        'typescript',
        'jsx',
        'decorators-legacy',
        'classProperties',
        'asyncGenerators',
        'dynamicImport',
        'optionalChaining',
        'nullishCoalescingOperator'
      ]
    });

    // 文件节点
    const fileNodeId = generateId('file', relativePath);
    const fileNode: CodeNode = {
      id: fileNodeId,
      type: NodeType.FILE,
      name: relativePath.split('/').pop() || relativePath,
      filePath: relativePath,
      lineStart: 1,
      lineEnd: fileInfo.lines,
      language: fileInfo.language,
      metadata: {
        size: fileInfo.size,
        lines: fileInfo.lines
      }
    };
    nodes.push(fileNode);

    // 遍历 AST
    traverse(ast, {
      // 导入声明
      ImportDeclaration(path) {
        const node = path.node;
        const source = node.source.value;
        const importNodeId = generateId('import', relativePath, source, path.node.loc?.start.line || 0);
        
        const importNode: CodeNode = {
          id: importNodeId,
          type: NodeType.IMPORT,
          name: source,
          filePath: relativePath,
          lineStart: node.loc?.start.line || 0,
          lineEnd: node.loc?.end.line || 0,
          language: fileInfo.language,
          metadata: { source }
        };
        nodes.push(importNode);

        // 文件 -> 导入关系
        edges.push({
          id: generateId('edge', fileNodeId, importNodeId),
          source: fileNodeId,
          target: importNodeId,
          type: EdgeType.IMPORTS
        });

        // 导入 -> 文件关系（解析具体导入）
        node.specifiers.forEach((spec, idx) => {
          if (t.isImportSpecifier(spec) || t.isImportDefaultSpecifier(spec)) {
            const localName = spec.local.name;
            const importedName = t.isImportSpecifier(spec) && spec.imported 
              ? (t.isIdentifier(spec.imported) ? spec.imported.name : spec.imported.value)
              : localName;

            const varNodeId = generateId('var', relativePath, localName, path.node.loc?.start.line || 0);
            const varNode: CodeNode = {
              id: varNodeId,
              type: NodeType.VARIABLE,
              name: localName,
              filePath: relativePath,
              lineStart: node.loc?.start.line || 0,
              lineEnd: node.loc?.end.line || 0,
              language: fileInfo.language,
              metadata: { 
                importedFrom: source,
                importedName: importedName
              }
            };
            nodes.push(varNode);

            edges.push({
              id: generateId('edge', importNodeId, varNodeId),
              source: importNodeId,
              target: varNodeId,
              type: EdgeType.REFERENCES
            });
          }
        });
      },

      // 函数声明
      FunctionDeclaration(path) {
        const node = path.node;
        if (!node.id) return;

        const funcName = node.id.name;
        const funcNodeId = generateId('func', relativePath, funcName, node.loc?.start.line || 0);
        
        const funcNode: CodeNode = {
          id: funcNodeId,
          type: NodeType.FUNCTION,
          name: funcName,
          filePath: relativePath,
          lineStart: node.loc?.start.line || 0,
          lineEnd: node.loc?.end.line || 0,
          language: fileInfo.language,
          metadata: {
            async: node.async,
            generator: node.generator,
            params: node.params.map(p => t.isIdentifier(p) ? p.name : 'param')
          }
        };
        nodes.push(funcNode);

        // 文件包含函数
        edges.push({
          id: generateId('edge', fileNodeId, funcNodeId),
          source: fileNodeId,
          target: funcNodeId,
          type: EdgeType.CONTAINS
        });
      },

      // 类声明
      ClassDeclaration(path) {
        const node = path.node;
        if (!node.id) return;

        const className = node.id.name;
        const classNodeId = generateId('class', relativePath, className, node.loc?.start.line || 0);
        
        const classNode: CodeNode = {
          id: classNodeId,
          type: NodeType.CLASS,
          name: className,
          filePath: relativePath,
          lineStart: node.loc?.start.line || 0,
          lineEnd: node.loc?.end.line || 0,
          language: fileInfo.language,
          metadata: {}
        };
        nodes.push(classNode);

        // 文件包含类
        edges.push({
          id: generateId('edge', fileNodeId, classNodeId),
          source: fileNodeId,
          target: classNodeId,
          type: EdgeType.CONTAINS
        });

        // 继承关系
        if (node.superClass && t.isIdentifier(node.superClass)) {
          edges.push({
            id: generateId('edge', classNodeId, node.superClass.name),
            source: classNodeId,
            target: generateId('class', relativePath, node.superClass.name, 0),
            type: EdgeType.EXTENDS
          });
        }

        // 处理方法
        path.node.body.body.forEach(member => {
          if (t.isClassMethod(member) && t.isIdentifier(member.key)) {
            const methodName = member.key.name;
            const methodNodeId = generateId('method', relativePath, className, methodName, member.loc?.start.line || 0);
            
            const methodNode: CodeNode = {
              id: methodNodeId,
              type: NodeType.METHOD,
              name: methodName,
              filePath: relativePath,
              lineStart: member.loc?.start.line || 0,
              lineEnd: member.loc?.end.line || 0,
              language: fileInfo.language,
              metadata: {
                kind: member.kind,
                async: member.async,
                static: member.static,
                className
              }
            };
            nodes.push(methodNode);

            edges.push({
              id: generateId('edge', classNodeId, methodNodeId),
              source: classNodeId,
              target: methodNodeId,
              type: EdgeType.CONTAINS
            });
          }
        });
      },

      // 接口声明
      TSInterfaceDeclaration(path) {
        const node = path.node;
        const interfaceName = node.id.name;
        const interfaceNodeId = generateId('interface', relativePath, interfaceName, node.loc?.start.line || 0);
        
        const interfaceNode: CodeNode = {
          id: interfaceNodeId,
          type: NodeType.INTERFACE,
          name: interfaceName,
          filePath: relativePath,
          lineStart: node.loc?.start.line || 0,
          lineEnd: node.loc?.end.line || 0,
          language: fileInfo.language,
          metadata: {}
        };
        nodes.push(interfaceNode);

        edges.push({
          id: generateId('edge', fileNodeId, interfaceNodeId),
          source: fileNodeId,
          target: interfaceNodeId,
          type: EdgeType.CONTAINS
        });
      },

      // 导出声明
      ExportNamedDeclaration(path) {
        const node = path.node;
        if (!node.declaration) return;

        const exportNodeId = generateId('export', relativePath, path.node.loc?.start.line || 0);
        
        let exportName = '';
        if (t.isFunctionDeclaration(node.declaration) && node.declaration.id) {
          exportName = node.declaration.id.name;
        } else if (t.isClassDeclaration(node.declaration) && node.declaration.id) {
          exportName = node.declaration.id.name;
        } else if (t.isVariableDeclaration(node.declaration)) {
          exportName = node.declaration.declarations.map(d => 
            t.isIdentifier(d.id) ? d.id.name : 'unknown'
          ).join(', ');
        }

        const exportNode: CodeNode = {
          id: exportNodeId,
          type: NodeType.EXPORT,
          name: exportName || 'anonymous',
          filePath: relativePath,
          lineStart: node.loc?.start.line || 0,
          lineEnd: node.loc?.end.line || 0,
          language: fileInfo.language,
          metadata: { exportName }
        };
        nodes.push(exportNode);

        edges.push({
          id: generateId('edge', fileNodeId, exportNodeId),
          source: fileNodeId,
          target: exportNodeId,
          type: EdgeType.EXPORTS
        });
      }
    });

  } catch (error) {
    console.error(`解析文件失败: ${fileInfo.path}`, error);
  }

  return { nodes, edges };
}