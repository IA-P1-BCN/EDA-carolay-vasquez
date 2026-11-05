"""Pipeline reproducible de un solo comando.

Encadena ingesta -> limpieza -> feature engineering -> guardado del dataset
limpio. Ejecutable con:

    python -m eda_covid.pipeline

Opciones:
    --refresh        fuerza volver a descargar los datos de la API.
    --raw PATH       ruta del CSV crudo (caché de ingesta).
    --out PATH       ruta de salida del CSV limpio.
    --umbral-nulos   umbral de proporción de nulos para descartar columnas.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from eda_covid import clean, features, ingest

DEFAULT_OUT = Path("data/processed/covid_clean.csv")


def run(
    raw_path: str | Path = ingest.DEFAULT_RAW_PATH,
    out_path: str | Path = DEFAULT_OUT,
    refresh: bool = False,
    umbral_nulos: float = clean.UMBRAL_NULOS_DEFECTO,
) -> Path:
    """Ejecuta el pipeline completo y devuelve la ruta del CSV limpio."""
    out_path = Path(out_path)

    print("[1/4] Ingesta de datos crudos...")
    crudo = ingest.load_raw(cache_path=raw_path, refresh=refresh)
    print(f"      {len(crudo)} filas x {crudo.shape[1]} columnas")

    print("[2/4] Limpieza...")
    limpio = clean.clean_dataset(crudo, umbral_nulos=umbral_nulos)
    print(f"      {len(limpio)} filas x {limpio.shape[1]} columnas tras limpiar")

    print("[3/4] Feature engineering + merge con poblacion...")
    enriquecido = features.construir_features(limpio)
    print(f"      {enriquecido.shape[1]} columnas tras features")

    print("[4/4] Guardando dataset limpio...")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    enriquecido.to_csv(out_path, index=False)
    print(f"      guardado en {out_path}")
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pipeline EDA COVID-19")
    parser.add_argument("--refresh", action="store_true", help="volver a descargar")
    parser.add_argument("--raw", default=str(ingest.DEFAULT_RAW_PATH))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--umbral-nulos", type=float, default=clean.UMBRAL_NULOS_DEFECTO)
    args = parser.parse_args(argv)

    run(
        raw_path=args.raw,
        out_path=args.out,
        refresh=args.refresh,
        umbral_nulos=args.umbral_nulos,
    )
    print("Pipeline completado con exito.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
