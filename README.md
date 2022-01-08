# tr-vaccine-bot
## _Vaccination counts for Turkey, in Telegram_


A bot for reporting daily vaccination counts through Telegram (for Covid-19 vaccines)
for Turkey. Data is parsed from Ministry of Health: https://covid19.saglik.gov.tr.

- Uses [telebot] for Telegram interfacing.
- [Selenium] Chrome Webdriver for data parsing.
- [Flask] web server for keeping the bot alive.

## Commands

- ```/hello```: Bot says hello.
- ```/asi```: Reports daily and total vaccination counts as a summarized text message. Also official and calculated vaccination rates in the population are given.
- At the time, daily reports can only be received via command, automated daily reports are WIP.

## License

GNU General Public License v3.0


   [telebot]: <https://github.com/eternnoir/pyTelegramBotAPI>
   [Selenium]: <https://selenium-python.readthedocs.io>
   [Flask]: <https://flask.palletsprojects.com/en/2.0.x/>
   
