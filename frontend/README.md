# TON DNS Checker Frontend

这是 TON DNS Checker 的前端部分。下面是安装和运行的指南。

## 安装

在开始之前，请确保您的机器上安装了 Node.js。

### 开发服务器

要在本地启动开发服务器，请执行以下步骤：

1. **安装依赖**:
   ```bash
   yarn install
   ```

2. **启动开发服务器**:
   ```bash
   yarn start
   ```

3. **访问应用**:
   打开浏览器并访问 [http://localhost:3000](http://localhost:3000)。

   **注意**: 确保在 `src/tools/fetchData.ts` 中设置了 `API_URL`，以指向有效的 api-dns 后端。

### 生产构建

要为生产环境构建应用，请执行以下步骤：

1. **构建应用**:
   ```bash
   yarn build
   ```

   这将把应用构建到 `build` 文件夹。

2. **部署应用**:
   您可以将 `build` 文件夹托管在您自己的 Web 服务器上。
