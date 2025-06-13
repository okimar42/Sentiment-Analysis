import '@testing-library/jest-dom'; 

// Stub ResizeObserver for charts in jsdom
class ResizeObserverStub {
  observe() {}
  unobserve() {}
  disconnect() {}
}
// @ts-ignore
global.ResizeObserver = global.ResizeObserver || ResizeObserverStub;

const __ES_INSTANCES__ = [];
class EventSourceStub {
  constructor(_url, _config) {
    this.onmessage = null;
    this.onerror = null;
    __ES_INSTANCES__.push(this);
  }
  close() {}
  // helper to simulate messages in tests
  emit(data) { if (this.onmessage) this.onmessage({ data }); }
}
// @ts-ignore
global.EventSource = global.EventSource || EventSourceStub;

// expose instances for tests
// @ts-ignore
global.__ES_INSTANCES__ = __ES_INSTANCES__; 