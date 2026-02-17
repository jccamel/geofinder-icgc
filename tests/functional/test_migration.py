#!/usr/bin/env python
"""
Script de prueba para verificar la migración a requests
"""


from geofinder import GeoFinder, PeliasError


async def test_basic_search():
    """Prueba búsqueda básica"""
    print("🔍 Probando búsqueda básica...")
    gf = GeoFinder()

    try:
        results = await gf.find("Barcelona")
        if results:
            print(f"✅ Encontrados {len(results)} resultados")
            print(f"   Primer resultado: {results[0]['nom']} - {results[0]['nomTipus']}")
        else:
            print("⚠️  No se encontraron resultados")
    except PeliasError as e:
        print(f"❌ Error Pelias: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        await gf.close()

async def test_coordinates():
    """Prueba búsqueda por coordenadas"""
    print("\n📍 Probando búsqueda por coordenadas...")
    gf = GeoFinder()

    try:
        results = await gf.find("430000 4580000 EPSG:25831")
        if results:
            print(f"✅ Encontrados {len(results)} resultados")
            for r in results[:3]:
                print(f"   - {r['nom']} ({r['nomTipus']})")
        else:
            print("⚠️  No se encontraron resultados")
    except PeliasError as e:
        print(f"❌ Error Pelias: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        await gf.close()

async def test_reverse_geocoding():
    """Prueba geocodificación inversa"""
    print("\n🔄 Probando geocodificación inversa...")
    gf = GeoFinder()

    try:
        results = await gf.find_reverse(430000, 4580000, epsg=25831, size=3)
        if results:
            print(f"✅ Encontrados {len(results)} resultados")
            for r in results:
                print(f"   - {r['nom']} ({r['nomTipus']})")
        else:
            print("⚠️  No se encontraron resultados")
    except PeliasError as e:
        print(f"❌ Error Pelias: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        await gf.close()

async def test_autocomplete():
    """Prueba autocompletado"""
    print("\n💡 Probando autocompletado...")
    gf = GeoFinder()

    try:
        results = await gf.autocomplete("Montserr", size=5)
        if results:
            print(f"✅ Encontradas {len(results)} sugerencias")
            for r in results:
                print(f"   - {r['nom']} ({r['nomTipus']})")
        else:
            print("⚠️  No se encontraron sugerencias")
    except PeliasError as e:
        print(f"❌ Error Pelias: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        await gf.close()

async def test_context_manager():
    """Prueba uso como context manager"""
    print("\n🔧 Probando context manager...")
    from geofinder.pelias import PeliasClient

    try:
        async with PeliasClient("https://eines.icgc.cat") as client:
            result = await client.geocode("Barcelona", size=1)
            if result.get("features"):
                print("✅ Context manager funciona correctamente")
                print("   Sesión cerrada automáticamente")
            else:
                print("⚠️  No se obtuvieron resultados")
    except PeliasError as e:
        print(f"❌ Error Pelias: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Test de Migración a Requests")
    print("=" * 60)

    async def run_all():
        await test_basic_search()
        await test_coordinates()
        await test_reverse_geocoding()
        await test_autocomplete()
        await test_context_manager()

    import asyncio
    asyncio.run(run_all())

    print("\n" + "=" * 60)
    print("✅ Tests completados")
    print("=" * 60)
