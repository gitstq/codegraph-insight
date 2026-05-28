/**
 * 文件工具函数
 */
import * as fs from 'fs';
import * as path from 'path';
import { glob } from 'glob';
import { FileInfo } from '../types';

/** 语言映射 */
const EXTENSION_MAP: Record<string, string> = {
  '.ts': 'typescript',
  '.tsx': 'typescript',
  '.js': 'javascript',
  '.jsx': 'javascript',
  '.py': 'python',
  '.java': 'java',
  '.go': 'go',
  '.rs': 'rust',
  '.cpp': 'cpp',
  '.c': 'c',
  '.h': 'c',
  '.php': 'php',
  '.rb': 'ruby',
  '.swift': 'swift',
  '.kt': 'kotlin',
  '.scala': 'scala',
  '.vue': 'vue',
  '.json': 'json',
  '.md': 'markdown',
  '.yml': 'yaml',
  '.yaml': 'yaml'
};

/**
 * 获取文件语言类型
 */
export function getLanguage(filePath: string): string {
  const ext = path.extname(filePath).toLowerCase();
  return EXTENSION_MAP[ext] || 'unknown';
}

/**
 * 检查是否应包含该文件
 */
export function shouldIncludeFile(filePath: string, include?: string[], exclude?: string[]): boolean {
  // 默认排除的目录
  const defaultExcludes = [
    'node_modules',
    '.git',
    'dist',
    'build',
    'coverage',
    '.next',
    '.nuxt',
    'vendor',
    '__pycache__',
    '.venv',
    'venv'
  ];

  // 检查默认排除
  for (const exclude of defaultExcludes) {
    if (filePath.includes(exclude)) {
      return false;
    }
  }

  // 检查自定义排除
  if (exclude) {
    for (const pattern of exclude) {
      if (filePath.includes(pattern)) {
        return false;
      }
    }
  }

  // 检查包含模式
  if (include && include.length > 0) {
    return include.some(pattern => filePath.includes(pattern));
  }

  return true;
}

/**
 * 扫描项目文件
 */
export async function scanProject(projectPath: string, include?: string[], exclude?: string[]): Promise<string[]> {
  const absolutePath = path.resolve(projectPath);
  
  // 支持的文件扩展名
  const extensions = Object.keys(EXTENSION_MAP).join(',');
  const pattern = path.join(absolutePath, `**/*{${extensions}}`);
  
  const files = await glob(pattern, { 
    absolute: true,
    ignore: [
      '**/node_modules/**',
      '**/.git/**',
      '**/dist/**',
      '**/build/**',
      '**/coverage/**',
      '**/.next/**',
      '**/__pycache__/**'
    ]
  });

  return files.filter(file => shouldIncludeFile(file, include, exclude));
}

/**
 * 读取文件信息
 */
export function readFileInfo(filePath: string): FileInfo | null {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const stats = fs.statSync(filePath);
    const lines = content.split('\n').length;

    return {
      path: filePath,
      content,
      language: getLanguage(filePath),
      size: stats.size,
      lines
    };
  } catch (error) {
    console.error(`读取文件失败: ${filePath}`, error);
    return null;
  }
}

/**
 * 获取相对路径
 */
export function getRelativePath(absolutePath: string, projectRoot: string): string {
  return path.relative(projectRoot, absolutePath);
}

/**
 * 生成唯一ID
 */
export function generateId(prefix: string, ...parts: (string | number)[]): string {
  const hash = parts.join('_').replace(/[^a-zA-Z0-9]/g, '_');
  return `${prefix}_${hash}`;
}