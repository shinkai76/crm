module.exports = {
    baseUrl: process.env.NODE_ENV === "production" ? "./" : "/",
    css: {
        // 是否使用css分离插件 ExtractTextPlugin
        extract: true,
        // 开启 CSS source maps?
        sourceMap: false,
        // css预设器配置项
        loaderOptions: {},
        // 启用 CSS modules for all css / pre-processor files.
        modules: false
    },
    outputDir: "static",
    devServer: {
        proxy: {
            "/api": {
                target: "http://192.168.2.196:8940",
                ws: true,
                changeOrigin: true
            }
        }
    },
    assetsDir: './'
};
