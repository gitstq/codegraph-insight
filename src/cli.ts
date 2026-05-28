#!/usr/bin/env node
/**
 * CLI 入口
 */
import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { analyzeProject } from './analyzer';
import { startDashboardServer } from './server/dashboard';
import { AnalyzerConfig } from './types';

const program = new Command();

program
  .name('codegraph')
  .description('🔮 CodeGraph Insight - 智能代码知识图谱分析工具')
  .version('1.0.0');

program
  .command('analyze')
  .description('分析代码项目并生成知识图谱')
  .argument('<project-path>', '项目路径')
  .option('-o, --output <path>', '输出文件路径', '.codegraph/graph.json')
  .option('-i, --include <patterns>', '包含的文件模式（逗号分隔）')
  .option('-e, --exclude <patterns>', '排除的文件模式（逗号分隔）')
  .action(async (projectPath, options) => {
    try {
      const absolutePath = path.resolve(projectPath);
      
      if (!fs.existsSync(absolutePath)) {
        console.error(`❌ 错误: 路径不存在 ${absolutePath}`);
        process.exit(1);
      }

      const config: AnalyzerConfig = {
        include: options.include ? options.include.split(',') : undefined,
        exclude: options.exclude ? options.exclude.split(',') : undefined
      };

      const result = await analyzeProject(absolutePath, config);

      // 保存结果
      const outputPath = path.resolve(options.output);
      const outputDir = path.dirname(outputPath);
      
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      fs.writeFileSync(outputPath, JSON.stringify(result.graph, null, 2));
      
      console.log(`\n💾 知识图谱已保存: ${outputPath}`);
      console.log(`\n📊 分析结果:`);
      console.log(`   分析文件数: ${result.stats.filesAnalyzed}`);
      console.log(`   总节点数: ${result.stats.totalNodes}`);
      console.log(`   总边数: ${result.stats.totalEdges}`);
      console.log(`   耗时: ${result.stats.duration}ms`);

    } catch (error) {
      console.error('❌ 分析失败:', error);
      process.exit(1);
    }
  });

program
  .command('dashboard')
  .description('启动可视化仪表盘')
  .argument('<graph-file>', '知识图谱 JSON 文件路径')
  .option('-p, --port <port>', '服务器端口', '3000')
  .action((graphFile, options) => {
    try {
      const graphPath = path.resolve(graphFile);
      
      if (!fs.existsSync(graphPath)) {
        console.error(`❌ 错误: 图谱文件不存在 ${graphPath}`);
        console.log(`💡 提示: 先运行 'codegraph analyze <项目路径>' 生成图谱`);
        process.exit(1);
      }

      const graph = JSON.parse(fs.readFileSync(graphPath, 'utf-8'));
      startDashboardServer(graph, parseInt(options.port));

    } catch (error) {
      console.error('❌ 启动失败:', error);
      process.exit(1);
    }
  });

program
  .command('quick')
  .description('一键分析并启动仪表盘')
  .argument('<project-path>', '项目路径')
  .option('-p, --port <port>', '服务器端口', '3000')
  .option('-i, --include <patterns>', '包含的文件模式（逗号分隔）')
  .option('-e, --exclude <patterns>', '排除的文件模式（逗号分隔）')
  .action(async (projectPath, options) => {
    try {
      const absolutePath = path.resolve(projectPath);
      
      if (!fs.existsSync(absolutePath)) {
        console.error(`❌ 错误: 路径不存在 ${absolutePath}`);
        process.exit(1);
      }

      const config: AnalyzerConfig = {
        include: options.include ? options.include.split(',') : undefined,
        exclude: options.exclude ? options.exclude.split(',') : undefined
      };

      // 分析项目
      const result = await analyzeProject(absolutePath, config);

      // 保存结果
      const outputPath = path.join(process.cwd(), '.codegraph', 'graph.json');
      if (!fs.existsSync(path.dirname(outputPath))) {
        fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      }
      fs.writeFileSync(outputPath, JSON.stringify(result.graph, null, 2));

      console.log(`\n💾 知识图谱已保存: ${outputPath}`);

      // 启动仪表盘
      startDashboardServer(result.graph, parseInt(options.port));

    } catch (error) {
      console.error('❌ 执行失败:', error);
      process.exit(1);
    }
  });

program.parse();