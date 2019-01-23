const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./src/index.js",
  mode: "development",
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules|bower_components)/,
        loader: "babel-loader",
        options: { presets: ["@babel/env"] }
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
  },
  resolve: { extensions: ["*", ".js", ".jsx"] },
  output: {
    path: path.resolve(__dirname, "dist/"),
    publicPath: "/dist/",
    filename: "bundle.js"
  },
  devServer: {
    contentBase: path.join(__dirname, "public/"),
    port: 7070,
    publicPath: "http://localhost:7070/dist/",
    historyApiFallback: true,
    disableHostCheck: true,
    //hotOnly: true,
    //hot: true,
    //inline: false,
    host: '0.0.0.0',
    watchOptions: {
      poll: 1000
    }
  },
  plugins: [new webpack.HotModuleReplacementPlugin()]
};
