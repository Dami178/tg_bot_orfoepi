from telebot import types
import telebot
import config
from telebot.async_telebot import AsyncTeleBot


import random as rnd
import op


list_wrong={

}

slova_pep={

}
# markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# markup.add(types.KeyboardButton('reset'))

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
list_pepa=set()



@bot.message_handler(commands=['start'])
async def start(message):
    slova_pep[message.chat.id]={}
    list_pepa.add(message.chat.username)
    print(list_pepa)

    await bot.send_message(message.chat.id,text='Тренируй свою грамотность с этим ботом! ✍️📚 \nПроверяй знания орфоэпии и улучшай произношение сложных слов. 🔤🗣️\n Для того чтобы сбросить решенные задания напишите /start',reply_markup=start_keyboard)






@bot.callback_query_handler(func=lambda callback:'run' in callback.data)
async def sort(callback):

    if callback.data in 'run':
        chs=rnd.randint(0,len(list_slov)-1)


        slova_pep[callback.message.chat.id][chs]=0



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

        word=list_slov[chs]

        rand=rnd.randint(0,1)
        rand_2=1 if rand==0 else 0

        word_keyboard=types.InlineKeyboardMarkup()
        word_keyboard.row(
            types.InlineKeyboardButton(word[rand],callback_data=f'k{word[rand]} {word[0]} {chs}'),
            types.InlineKeyboardButton(word[rand_2],callback_data=f'k{word[rand_2]} {word[0]} {chs}')
        )
        await bot.send_message(callback.message.chat.id,text='Какое произношение правильное? 🤔🔠',reply_markup=word_keyboard)


#Прорешивание ОШИБОК
@bot.callback_query_handler(func=lambda callback:'yes' in callback.data or 'no' in callback.data )
async def pepa(callback):

    if callback.data=='yes' or 'c' in callback.data:

        if callback.data=='yes':
            lsit_wrong=[]
            for i in slova_pep[callback.message.chat.id]:
                if slova_pep[callback.message.chat.id][i]==0:
                    lsit_wrong.append(i)
            list_wrong[callback.message.chat.id]=lsit_wrong
            print('lsit_wrong',lsit_wrong)



        if len(list_wrong[callback.message.chat.id])==0:
            await bot.send_message(callback.message.chat.id,text='Все слова приволб',reply_markup=word_keyboard)

        print(list_wrong)


        rand=rnd.randint(0,1)
        rand_2=1 if rand==0 else 0


        word=list_slov[list_wrong[callback.message.chat.id][0]]
        print('word',word)


        word_keyboard=types.InlineKeyboardMarkup()
        word_keyboard.row(
            types.InlineKeyboardButton(word[rand],callback_data=f'c{word[rand]} {word[0]}'),
            types.InlineKeyboardButton(word[rand_2],callback_data=f'c{word[rand_2]} {word[0]}')
        )
        await bot.send_message(callback.message.chat.id,text='Какое произношение правильное? 🤔🔠',reply_markup=word_keyboard)




    else:
        await bot.send_message(callback.message.chat.id,text='Для того чтобы начать заново напишите /start')



@bot.callback_query_handler(func=lambda callback:'c' in callback.data)
async def corrections(callback):

    s=callback.data[1:]

    a=s.split(' ')
    print('s',s)
    print('Проверка',a)


    if a[0]==a[1]:

        await bot.send_message(callback.message.chat.id,text='Верно!✅ Так держать! 💪✨')
        print('После верно',list_wrong[callback.message.chat.id])

        list_wrong[callback.message.chat.id]=list_wrong[callback.message.chat.id][1:]

        print('После уменьшения',list_wrong[callback.message.chat.id])

        if len(list_wrong[callback.message.chat.id])==0:
            await bot.send_message(callback.message.chat.id,text='Все слова исправлены \n Для того чтобы решать ещё раз напишите /start')

            slova_pep[callback.message.chat.id]={}

        else:

            await pepa(callback)


    else:

        await bot.send_message(callback.message.chat.id,text=f'Не правильно ❌ \nПравильное произношение: {a[1]} ✅')
        list_wrong[callback.message.chat.id]=list_wrong[callback.message.chat.id][1:]

        await pepa(callback)

import asyncio

asyncio.run(bot.polling(none_stop=True))
