import { app, BrowserWindow } from 'electron'
import { spawn } from 'child_process'
import fetch from 'node-fetch'
import portfinder from 'portfinder'
import path from 'path'
import { fileURLToPath } from 'url'

const dir = path.dirname(fileURLToPath(import.meta.url))

app.on('window-all-closed', function () {
    app.quit()
})

function spawnPyUnix(dir, port) {
    return spawn('.venv/bin/python', ['server.py', dir + '/frontend', port], { cwd: dir + '/backend', stdio: 'inherit' })
}

function spawnPyWindows(dir, port) {
    return spawn('.venv/Scripts/python.exe', ['server.py', dir + '/frontend', port], {
        cwd: dir + '/backend',
        stdio: 'inherit'
    })
}

function spawnPy(dir, port) {
    const subpy = spawnPyWindows(dir, ['server.py', dir + '/frontend', port], {})

    subpy.on('error', function () {
        spawnPyUnix(dir, port)
    })

    return subpy
}

app.on('ready', function () {
    portfinder.getPort(function (_err, port) {
        const subpy = spawnPy(dir, port)

        const mainAddr = 'http://localhost:' + port

        const startUp = function () {
            fetch(mainAddr)
                .then(function () {
                    const mainWindow = new BrowserWindow({ width: 800, height: 600 })
                    mainWindow.loadURL(mainAddr)
                    mainWindow.on('closed', function () {
                        subpy.kill('SIGINT')
                    })
                })
                .catch(function () {
                    startUp()
                })
        }

        startUp()
    })
})
