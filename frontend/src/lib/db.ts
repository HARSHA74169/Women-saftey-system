export interface Emotion {
  id: number;
  timestamp: string;
  emotion: string;
  confidence: number;
  steps: number;
}

export interface Alert {
  id: number;
  timestamp: string;
  type: string;
  message: string;
  acknowledged: boolean;
}

const DB_NAME = 'emotionTracker';
const DB_VERSION = 1;

const openDB = (): Promise<IDBDatabase> => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;

      // Create emotions store
      if (!db.objectStoreNames.contains('emotions')) {
        const emotionsStore = db.createObjectStore('emotions', { keyPath: 'id', autoIncrement: true });
        emotionsStore.createIndex('timestamp', 'timestamp');
      }

      // Create alerts store
      if (!db.objectStoreNames.contains('alerts')) {
        const alertsStore = db.createObjectStore('alerts', { keyPath: 'id', autoIncrement: true });
        alertsStore.createIndex('timestamp', 'timestamp');
      }
    };
  });
};

export const getLatestEmotions = async (): Promise<Emotion[]> => {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction('emotions', 'readonly');
    const store = transaction.objectStore('emotions');
    const request = store.index('timestamp').openCursor(null, 'prev');
    const emotions: Emotion[] = [];

    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const cursor = request.result;
      if (cursor && emotions.length < 20) {
        emotions.push(cursor.value);
        cursor.continue();
      } else {
        resolve(emotions);
      }
    };
  });
};

export const getLatestAlerts = async (): Promise<Alert[]> => {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction('alerts', 'readonly');
    const store = transaction.objectStore('alerts');
    const request = store.index('timestamp').openCursor(null, 'prev');
    const alerts: Alert[] = [];

    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const cursor = request.result;
      if (cursor && alerts.length < 20) {
        alerts.push(cursor.value);
        cursor.continue();
      } else {
        resolve(alerts);
      }
    };
  });
};

export const addEmotion = async (emotion: string, confidence: number, steps: number): Promise<void> => {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction('emotions', 'readwrite');
    const store = transaction.objectStore('emotions');
    const request = store.add({
      timestamp: new Date().toISOString(),
      emotion,
      confidence,
      steps
    });

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve();
  });
};

export const addAlert = async (type: string, message: string): Promise<void> => {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction('alerts', 'readwrite');
    const store = transaction.objectStore('alerts');
    const request = store.add({
      timestamp: new Date().toISOString(),
      type,
      message,
      acknowledged: false
    });

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve();
  });
};