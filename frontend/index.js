import { app, BrowserWindow } from 'electron'

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        titleBarStyle: 'hidden',
    })

    win.loadURL('http://localhost:8000/')
}

app.whenReady().then(() => {
    createWindow()
})
