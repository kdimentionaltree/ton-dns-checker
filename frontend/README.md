# TON DNS Checker[frontend]

## Install

### Dev server(node js on your machine required):

`yarn install && yarn start`

[http://localhost:3000](http://localhost:3000) - stand.
Set API_URL in `src/tools/fetchData.ts` to valid api-dns backend to run frontend dev-server.

### Production build(node js on your machine required):

`yarn build`

Builds the app for production to the `build` folder.\
Then you can host `build` folder on your own web server.
