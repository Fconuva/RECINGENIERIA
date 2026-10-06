// ============================================================
//  Genera assets/firebase-env.js a partir de variables de entorno.
//  Se ejecuta automáticamente en Vercel (buildCommand de vercel.json).
//  Si no hay variables definidas (p. ej. en local), no hace nada y
//  el sitio usa los valores de respaldo de assets/firebase-config.js.
// ============================================================
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const out = join(__dirname, "..", "assets", "firebase-env.js");

const cfg = {
  apiKey:            process.env.FIREBASE_API_KEY,
  authDomain:        process.env.FIREBASE_AUTH_DOMAIN,
  projectId:         process.env.FIREBASE_PROJECT_ID,
  storageBucket:     process.env.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
  appId:             process.env.FIREBASE_APP_ID,
};

const hayAlgo = Object.values(cfg).some(Boolean);

if (!hayAlgo) {
  writeFileSync(out, "/* Sin variables de entorno: se usan los valores de firebase-config.js */\n");
  console.log("[firebase-env] No hay variables FIREBASE_* definidas; se usa el respaldo embebido.");
} else {
  // Solo incluir las claves que vengan definidas, para no pisar el respaldo con undefined.
  const limpio = Object.fromEntries(Object.entries(cfg).filter(([, v]) => Boolean(v)));
  const js = "window.__FIREBASE_CONFIG__ = " + JSON.stringify(limpio, null, 2) + ";\n";
  writeFileSync(out, js);
  console.log("[firebase-env] firebase-env.js generado con:", Object.keys(limpio).join(", "));
}
