const TerserPlugin = require("terser-webpack-plugin");

var path = require("path");

// Custom webpack rules are generally the same for all webpack bundles, hence
// stored in a separate local variable.
var rules = [
  { test: /\.css$/, use: ["style-loader", "css-loader"] },
  { test: /\.svg$/, use: ["svg-inline-loader"] }
];

var minimize = false;

module.exports = {
  entry: "./lib/index.js",
  output: {
    filename: "index.js",
    path: path.resolve(__dirname, "dist"),
    publicPath: "auto",
    library: {
      name: "CadViewerWidget",
      type: "window"
    }
  },
  devtool: false,
  resolve: { extensions: [".js", ".json"] },
  optimization: {
    minimize: minimize,
    minimizer: [
      new TerserPlugin({
        parallel: true,
        terserOptions: {
          compress: { defaults: false },
          mangle: false
        }
      })
    ]
  },
  module: {
    rules: rules
  }
};
