# 使用 Node.js 作為構建環境
FROM node:latest as build

# 設置工作目錄
WORKDIR /app

# 複製 package.json 和 yarn.lock 文件
COPY package.json yarn.lock ./

# 安裝依賴
RUN yarn install

# 複製其餘的應用源代碼
COPY . .

# 構建應用
RUN yarn build

# 使用 Nginx 作為服務器
FROM nginx:alpine

# 複製構建好的應用文件
COPY --from=build /app/build /usr/share/nginx/html

# 暴露 80 端口
EXPOSE 80

# 啟動 Nginx 並保持前台運行
CMD ["nginx", "-g", "daemon off;"]
