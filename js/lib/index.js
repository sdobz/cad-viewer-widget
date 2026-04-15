// Export the framework-neutral viewer runtime and the npm package version.

// eslint-disable-next-line no-undef
var widgetExports = require("./widget.js");

function normalizeState(state) {
  if (!state || typeof state !== "object") {
    return {};
  }

  const next = { ...state };
  if (next.newTreeBehavior == null && next.new_tree_behavior != null) {
    next.newTreeBehavior = next.new_tree_behavior;
  }
  if (next.initialize == null) {
    next.initialize = false;
  }
  return next;
}

function mountCadViewer(element, state) {
  if (!element) {
    throw new Error("mountCadViewer requires a target element");
  }

  const model = new widgetExports.CadViewerModel(normalizeState(state));
  const view = new widgetExports.CadViewerView({ model: model, el: element });

  view.render();
  view.showViewer();
  view.addShapes();

  return { model, view };
}

// eslint-disable-next-line no-undef
module.exports = { ...widgetExports, mountCadViewer };

// eslint-disable-next-line no-undef
module.exports["version"] = require("../package.json").version;
