# FlowerOptimizer

一个帮助您自定义选择花云入口的小工具。

## 安装

### Windows

您可以在 [Github Release](https://github.com/ProjectAegle/FlowerOptimizer/releases) 中下载预构建的程序，解压缩后直接运行即可使用，无需安装，运行后会自动输出 Web 控制面板地址，但我们建议您在系统中安装服务后使用，您可以在控制面板中一键安装服务。

### 所有操作系统

您可以直接下载源代码包，之后运行 `sanic flower_optimizer.api`，请注意，您需要 Python 3 环境，并安装 `niquests` 和 `sanic` 包。

我们不对其他操作系统提供服务支持，请不要试图使用服务面板中的功能，您可以使用 `systemd` 等管理系统添加服务。
