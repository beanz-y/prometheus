# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('engine', 'engine'), ('content', 'content'), ('story', 'story'), ('VERSION', '.')],
    hiddenimports=['content', 'content.intro', 'content.rooms_act1', 'content.rooms_act2', 'content.rooms_act3', 'content.items', 'content.npcs', 'content.dialogues', 'content.events', 'content.endings', 'content.memories', 'content.puzzles', 'content.companion_lines', 'engine', 'engine.game', 'engine.parser', 'engine.display', 'engine.world', 'engine.room', 'engine.item', 'engine.npc', 'engine.player', 'engine.event', 'engine.dialogue', 'engine.save_load', 'engine.companion'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ThePrometheusProtocol',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ThePrometheusProtocol',
)
