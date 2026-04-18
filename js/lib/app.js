var _cellViewers = {};
var _currentCadViewer = null;

export default {
  getCadViewers() {
    return {
      cell: _cellViewers
    };
  },

  getCurrentViewer() {
    return _currentCadViewer;
  },

  setCurrentViewer(viewer) {
    _currentCadViewer = viewer;
  },

  addCellViewer(id, viewer) {
    _currentCadViewer = viewer;
    _cellViewers[id] = viewer;
    console.log(`cad-viewer-widget: Cell viewer ${id} created`);
  },

  cleanupCellViewers() {
    for (const [id, viewer] of Object.entries(_cellViewers)) {
      const container = viewer?.container;
      const isAlive = container != null && container.isConnected;
      if (!isAlive) {
        viewer.dispose();
        delete _cellViewers[id];
        console.log(`cad-viewer-widget: Cell viewer "${id}" removed`);
      }
    }
  },

  removeCellViewer(id) {
    delete _cellViewers[id];
  }
};
