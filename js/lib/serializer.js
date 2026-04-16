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
  if (obj == null) {
    return obj;
  }
  const ab = toArrayBuffer(obj.buffer);
  if (obj.dtype === "float32") return new Float32Array(ab);
  if (obj.dtype === "uint32") return new Uint32Array(ab);
  if (obj.dtype === "int32") return new Int32Array(ab);
  throw new Error("cad-viewer-widget: unknown dtype " + obj.dtype);
}

function maybeConvertBuffer(obj) {
  if (obj == null) {
    return obj;
  }
  if (ArrayBuffer.isView(obj) || obj instanceof ArrayBuffer) {
    return obj;
  }
  if (typeof obj === "object" && obj.buffer != null && obj.dtype != null) {
    return convertBuffer(obj);
  }
  return obj;
}

function resolveShapeRef(shape, instances) {
  if (
    shape != null &&
    typeof shape === "object" &&
    typeof shape.ref === "number" &&
    Array.isArray(instances)
  ) {
    return instances[shape.ref] ?? null;
  }
  return shape;
}

// data = { data: { shapes: <tree>, states: { "/id": [1,1], ... } } }
// Mutates the tree in-place: converts buffer descriptors to typed arrays
// and attaches state from the states map to each node.
function decode(data) {
  const payload = data.data;
  const stateMap = payload.states || {};
  const instances = Array.isArray(payload.instances) ? payload.instances : [];

  instances.forEach((instance) => {
    if (!instance || typeof instance !== "object") {
      return;
    }
    instance.vertices = maybeConvertBuffer(instance.vertices);
    instance.normals = maybeConvertBuffer(instance.normals);
    instance.triangles = maybeConvertBuffer(instance.triangles);
    instance.obj_vertices = maybeConvertBuffer(instance.obj_vertices);
    instance.face_types = maybeConvertBuffer(instance.face_types);
    instance.edge_types = maybeConvertBuffer(instance.edge_types);
    instance.triangles_per_face = maybeConvertBuffer(instance.triangles_per_face);
    instance.segments_per_edge = maybeConvertBuffer(instance.segments_per_edge);
    instance.edges = maybeConvertBuffer(instance.edges);
  });

  function walk(node) {
    if (Array.isArray(node)) {
      node.forEach(walk);
      return;
    }
    if (!node || typeof node !== "object") return;

    if (node.type === "shapes") {
      let s = resolveShapeRef(node.shape, instances);
      if (!s || typeof s !== "object") {
        throw new Error("cad-viewer-widget: invalid shape payload");
      }
      s.vertices = maybeConvertBuffer(s.vertices);
      s.normals = maybeConvertBuffer(s.normals);
      s.triangles = maybeConvertBuffer(s.triangles);
      s.edges = maybeConvertBuffer(s.edges);
      node.shape = s;
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
