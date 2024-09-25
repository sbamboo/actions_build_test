name: Pyinstaller Build Test
run-name: ${{ github.actor }} is building python code.
on: [push]
jobs:

  stage:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        cache: 'pip' # caching pip dependencies
    - run: pip install -r stage-requirements.txt
    - run: python staged/stage.py

    - uses: actions/upload-artifact@master
      with:
        name: fused
        path: staged/fused/staged.py

  linux:
    needs: stage
    runs-on: ubuntu-latest
    steps:
        
    - uses: actions/checkout@v4

    - uses: actions/download-artifact@master
      with:
        name: fused
        path: staged/fused/

    - run: ls staged/fused/

    - run: cat staged/fused/staged.py

    - uses: sayyid5416/pyinstaller@v1
      with:
        python_ver: '3.12'
        pyinstaller_ver: '==6.10.0'
        spec: 'staged/fused/staged.py'
        requirements: 'src/requirements.txt'
        upload_exe_with_name: 'linux_x86_64'
        options: --onefile, --name "Example App"

  windows:
    needs: stage
    runs-on: windows-2019
    steps:
        
    - uses: actions/checkout@v4

    - uses: actions/download-artifact@master
      with:
        name: fused
        path: staged/fused/staged.py

    - uses: sayyid5416/pyinstaller@v1
      with:
        python_ver: '3.12'
        pyinstaller_ver: '==6.10.0'
        spec: 'staged/fused/staged.py'
        requirements: 'src/requirements.txt'
        upload_exe_with_name: 'windows_x86_64'
        options: --onefile, --name "Example App"

  macos:
    needs: stage
    strategy:
      matrix:
        os-version: ['12', '14']
        include:
          - os-version: '12'
            arch: x86_64
          - os-version: '14'
            arch: aarch64
    runs-on: macos-${{ matrix.os-version }}
    env:
      # even though we run on 12, target towards compatibility
      MACOSX_DEPLOYMENT_TARGET: '11.0'
    steps:
        
    - uses: actions/checkout@v4

    - uses: actions/download-artifact@master
      with:
        name: fused
        path: staged/fused/staged.py
        
    - uses: sayyid5416/pyinstaller@v1
      with:
        python_ver: '3.12'
        pyinstaller_ver: '==6.10.0'
        spec: 'staged/fused/staged.py'
        requirements: 'src/requirements.txt'
        upload_exe_with_name: 'macos_${{ matrix.arch }}'
        options: --onefile, --name "Example App"