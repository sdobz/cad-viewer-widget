// Decode a binary buffer sent by anywidget (DataView / ArrayBuffer / Uint8Array / base64 string)
// into a contiguous ArrayBuffer ready for typed-array construction.
function toArrayBuffer(bufferLike) {
  if (typeof bufferLike === "string") {
    // anywidget encodes memoryview as base64
    const binary = atob(bufferLike);
    const u8 = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) u8[i] = binary.charCodeAt(i);
    return u8.buffer;
  }
  // DataView implements ArrayBufferView, so handle it first.
  if (ArrayBuffer.isView(bufferLike)) {
    const u8 = new Uint8Array(
      bufferLike.buffer,
      bufferLike.byteOffset,
      bufferLike.byteLength
    );
    return u8.byteOffset === 0 && u8.byteLength === u8.buffer.byteLength
      ? u8.buffer
      : u8.buffer.slice(u8.byteOffset, u8.byteOffset + u8.byteLength);
  }
  if (bufferLike instanceof ArrayBuffer) {
    return bufferLike;
  }
  throw new Error(
    "cad-viewer-widget: unexpected buffer type " +
      Object.prototype.toString.call(bufferLike)
  );
}

// Decode a typed-array buffer descriptor sent from Python via anywidget.
// obj = { shape: [N], dtype: "float32"|"uint32", buffer: <DataView|ArrayBuffer> }
function convertBuffer(obj) {
  const ab = toArrayBuffer(obj.buffer);
  if (obj.dtype === "float32") return new Float32Array(ab);
  if (obj.dtype === "uint32") return new Uint32Array(ab);
  if (obj.dtype === "int32") return new Int32Array(ab);
  throw new Error("cad-viewer-widget: unknown dtype " + obj.dtype);
}

// data = { data: { shapes: <tree>, states: { "/id": [1,1], ... } } }
// Mutates the tree in-place: converts buffer descriptors to typed arrays
// and attaches state from the states map to each node.
function decode(data) {
  const payload = data.data;
  const stateMap = payload.states || {};

  function walk(node) {
    if (Array.isArray(node)) {
      node.forEach(walk);
      return;
    }
    if (!node || typeof node !== "object") return;

    if (node.type === "shapes") {
      const s = node.shape;
      s.vertices = convertBuffer(s.vertices);
      s.normals = convertBuffer(s.normals);
      s.triangles = convertBuffer(s.triangles);
      // s.edges is a plain nested JS array produced by to_json — leave as-is
    }

    // Attach visibility state; default [faces visible, edges visible]
    node.state = stateMap[node.id] || [1, 1];

    if (Array.isArray(node.parts)) {
      node.parts.forEach(walk);
    }
  }

  walk(payload.shapes);
}

export { decode };
