// Export the framework-neutral viewer runtime and the npm package version.

// eslint-disable-next-line no-undef
var widgetExports = require("./widget.js");

// eslint-disable-next-line no-undef
module.exports = { ...widgetExports };

// eslint-disable-next-line no-undef
module.exports["version"] = require("../package.json").version;
