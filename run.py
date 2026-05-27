#!/usr/bin/env python3
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Запускаем бота
from nitro_bot import main

if __name__ == "__main__":
    main()