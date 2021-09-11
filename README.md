# calendar-zap --> Python + AWS S3 + Twilio (Whatsapp) + Heroku

## What is it?
- This whatsapp bot aims to facilitate the sharing of important dates on the Whatsapp platform, so that multiple people can manage the saved dates at the same time (or individually)
- The dates are saved in the AWS database (S3)
- The bot uses Twilio to manage Whatsapp messages (received/sent)
- The app is deployed in Heroku

## How it works

![](img/calendarzap.gif)

- When sharing the bot, there is one more feature where the bot notifies you at the end of the day if someone has added or deleted a date.
![image](https://user-images.githubusercontent.com/61205851/132929014-221ab593-9df5-4716-9d49-dee5767479f2.png)

## Commands
```
Salvar:
  - salvar xx/yy exemplo 1.
  - save xx/yy exemplo 1.
  
Deletar:
  - del xx/yy exemplo 1.
  
Mostrar as datas:
  - datas
  - show
  
```
