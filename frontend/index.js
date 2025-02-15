import connect from 'connect'
import serveStatic from 'serve-static'
import { app, BrowserWindow } from 'electron'

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        titleBarStyle: 'hidden',
    })

    win.loadFile('index.html')
    win.loadURL('http://localhost:8080/')
}
// Loads up the server
connect()
    .use(serveStatic('./'))
    .listen(8080, () => {
        console.log('Server running on 8080...')
        app.whenReady().then(() => {
            createWindow()
        })
    })
