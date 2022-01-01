import qrcode

link = 'https://sam-myportfolio.web.app'
url = qrcode.make(link)
url.save('myqr.png')