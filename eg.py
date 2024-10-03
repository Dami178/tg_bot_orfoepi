from telebot import types
import telebot
import config
from telebot.async_telebot import AsyncTeleBot
import keyboard as keyb
import pyperclip
import random as rnd
import op




slova_pep={
    
}


start_keyboard=types.InlineKeyboardMarkup()
start_keyboard.row(
    types.InlineKeyboardButton('Начать',callback_data='run')
)


repeat_keyboard=types.InlineKeyboardMarkup()
repeat_keyboard.row(
    types.InlineKeyboardButton('Да',callback_data='yes'),
    types.InlineKeyboardButton('Нет',callback_data='no')
)


bot = AsyncTeleBot(config.Token)

list_slov=op.a




@bot.message_handler(commands=['start'])
async def start(message):
    slova_pep[message.chat.id]={}
    await bot.send_message(message.chat.id,text='Тренируй свою грамотность с этим ботом! ✍️📚 \nПроверяй знания орфоэпии и улучшай произношение сложных слов. 🔤🗣️',reply_markup=start_keyboard)
    

@bot.callback_query_handler(func=lambda callback:'run' in callback.data)
async def sort(callback):

    if callback.data in 'run':
        chs=rnd.randint(0,len(list_slov)-1)


        slova_pep[callback.message.chat.id][chs]=0
        print(slova_pep)

        
        word=list_slov[chs]

        rand=rnd.randint(0,1)
        rand_2=1 if rand==0 else 0
        
        word_keyboard=types.InlineKeyboardMarkup()
        word_keyboard.row(
            types.InlineKeyboardButton(word[rand],callback_data=f'k{word[rand]} {word[0]} {chs}'),
            types.InlineKeyboardButton(word[rand_2],callback_data=f'k{word[rand_2]} {word[0]} {chs}')
        )
        

        await bot.send_message(callback.message.chat.id,text='Какое произношение правильное? 🤔🔠',reply_markup=word_keyboard)

@bot.callback_query_handler(func=lambda callback:'k' in callback.data or 'not' in callback.data)
async def check(callback):
    
    s=callback.data[1:]

    a=s.split()
    print(a)

    if a[0]==a[1]:
        
        await bot.send_message(callback.message.chat.id,text='Верно!✅ Так держать! 💪✨')
        slova_pep[callback.message.chat.id][int(a[2])]=1

    else:
        
        await bot.send_message(callback.message.chat.id,text=f'Не правильно ❌ \nПравильное произношение: {a[1]} ✅')
    



    chs=rnd.randint(0,len(list_slov)-1)
    while chs in slova_pep[callback.message.chat.id]:
        if len(slova_pep[callback.message.chat.id])==len(list_slov):

            await bot.send_message(callback.message.chat.id,text=f'Все слова прорешаны')

            await bot.send_message(callback.message.chat.id,text=f'Прорешаем слова в которых были ошибки?',reply_markup=repeat_keyboard)
            break
    
        chs=rnd.randint(0,len(list_slov)-1)
    
    if chs not in slova_pep[callback.message.chat.id]:
        
    
        slova_pep[callback.message.chat.id][chs]=0
        print(slova_pep)
        word=list_slov[chs]

        rand=rnd.randint(0,1)
        rand_2=1 if rand==0 else 0
        
        word_keyboard=types.InlineKeyboardMarkup()
        word_keyboard.row(
            types.InlineKeyboardButton(word[rand],callback_data=f'k{word[rand]} {word[0]} {chs}'),
            types.InlineKeyboardButton(word[rand_2],callback_data=f'k{word[rand_2]} {word[0]} {chs}')
        )
        await bot.send_message(callback.message.chat.id,text='Какое произношение правильное? 🤔🔠',reply_markup=word_keyboard)
    
@bot.callback_query_handler(func=lambda callback:'yes' in callback.data or 'no' in callback.data )
async def pepa(callback,list_wrong=''):
    print('pered ifom',list_wrong)
    if callback.data=='yes' or 'c' in callback.data:
        
        
        if list_wrong =='':
            
            for i in slova_pep[callback.message.chat.id]:
                if slova_pep[callback.message.chat.id][i]==0:
                    list_wrong+=f'{i}.'

        print('wdaadwadw',list_wrong)
        


        rand=rnd.randint(0,1)
        rand_2=1 if rand==0 else 0


        word=list_slov[int(list_wrong.split('.')[0])]
        print('slova',word)

        word_keyboard=types.InlineKeyboardMarkup()
        word_keyboard.row(
            types.InlineKeyboardButton(word[rand],callback_data=f'c{word[rand]} {word[0]} {list_wrong}'),
            types.InlineKeyboardButton(word[rand_2],callback_data=f'c{word[rand_2]} {word[0]} {list_wrong}')
        )
        await bot.send_message(callback.message.chat.id,text='Какое произношение правильное? 🤔🔠',reply_markup=word_keyboard)




    else:
        await bot.send_message(callback.message.chat.id,text='Ошибок не было! 💯',reply_markup=word_keyboard)
        
@bot.callback_query_handler(func=lambda callback:'c' in callback.data)
async def corrections(callback):
    print(52)
    s=callback.data[1:]

    a=s.split()
    
    list_wrong=a[2]
    if list_wrong.count('.')==1:
        list_wrong=list_wrong[:list_wrong.index('.')]
    else:
        list_wrong=list_wrong.split('.')
    print(a)
    
    if a[0]==a[1]:
        
        await bot.send_message(callback.message.chat.id,text='Верно!✅ Так держать! 💪✨')
        print('aaaa',list_wrong)

        if type(list_wrong)==str:
            await bot.send_message(callback.message.chat.id,text='Все слова исправлены \n Для того чтобы решать ещё раз напишите /start')
            
        else:
            list_wrong=list_wrong[1:-1]
            s=''
            for i in list_wrong:
                s+=f'{i}.'
            
            await pepa(callback,s)
        

    else:
        
        await bot.send_message(callback.message.chat.id,text=f'Не правильно ❌ \nПравильное произношение: {a[1]} ✅')
        list_wrong=list_wrong[1:-1]
        s=''
        for i in list_wrong:
            s+=f'{i}.'
        
        await pepa(callback,s)

import asyncio

asyncio.run(bot.polling(none_stop=True))




