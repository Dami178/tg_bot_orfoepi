from telebot import types
import telebot
import config
from telebot.async_telebot import AsyncTeleBot


import random 
import op

task_pep={

}
correct_task={

}

list_wrong={

}

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
list_pepa=set()

@bot.message_handler(commands=['clear'])
async def start(message):

    slova_pep[message.chat.id]={}
    await start(message)
    


@bot.message_handler(commands=['list'])
async def start(message):
    if message.chat.id==1037060726:
        
        s=''
        for i in list_pepa:s+=i
        
        await bot.send_message(message.chat.id,text=s)
        a= [f'{i} : {len([slova_pep[i][n] for n in slova_pep[i] if slova_pep[i][n]==1])} / {len(slova_pep[i])-1}'  for i in slova_pep]
        sk=''
        # await bot.send_message(message.chat.id,text=f'{slova_pep}') 
        for i in a:sk+=f'{i}\n'
        await bot.send_message(message.chat.id,text=f'{sk}') 
        sks=''
        
        for i in correct_task:sks+=f'{i} : {correct_task[i]}\n'
        await bot.send_message(message.chat.id,text=f'{sks}') 


@bot.message_handler(commands=['restart'])
async def start(message):
    if message.chat.id==1037060726:
        a=open('slova_p.txt','w')
         
        a.write(f'{slova_pep}\n')
        a.write(f'{list_pepa}\n')
        a.write(f'{task_pep}\n')
        a.write(f'{correct_task}')
        
        await bot.send_message(message.chat.id,text=f'Данные сохранены можете запускать рестарт! Когда перезапустите сервер напишите /return')

@bot.message_handler(commands=['return'])
async def start(message):
    if message.chat.id==1037060726:
        file=open('slova_p.txt','r').readlines()
        
        a=file[0][:-1]
        b=file[1][:-1]
        c=file[2][:-1]
        d=file[3]
        
        
        
        global slova_pep
        global list_pepa
        global task_pep
        global correct_task

        
        slova_pep=eval(a)
        list_pepa= eval(b)
        task_pep=eval(c)
        correct_task=eval(d)
        
        
        await bot.send_message(message.chat.id,text=f'Рестарт окончен, все данные возращены!')
@bot.message_handler(commands=['check'])
async def check(message):
    
    
    
    
    sk=f'Слова : {len([slova_pep[message.chat.id][n] for n in slova_pep[message.chat.id] if slova_pep[message.chat.id][n]==1])} / {len(slova_pep[message.chat.id])-1}'
    await bot.send_message(message.chat.id,text=f'{sk}') 
    
    sks= f'Задания из ЕГЭ : {correct_task[message.chat.id]}'
    
    await bot.send_message(message.chat.id,text=sks)
@bot.message_handler(commands=['task'])
async def task(message):
    
    
    k = random.randint(2,4)
    a=[]
    for i in range(5):
        kda=random.randint(0,len(list_slov)-1)
        while kda  in a:
            kda=random.randint(0,len(list_slov)-1)
        a.append(kda)

    
    
    list_task=[]
    for i in range(k):
        p=random.choice(a)

        list_task.append(list_slov[p][0])
        a.remove(p)
    
    dont_edit=list_task[:]
    for i in a:
        
        list_task.append(list_slov[i][1])
    

    random.shuffle(list_task)

    correct_answer=''

    for i in dont_edit:

        correct_answer+=f"{list_task.index(i)+1}"

    correct_answer=''.join(sorted(correct_answer))

    
    for i in range(len(list_task)):

        list_task[i]=f'{i+1}) {list_task[i]}\n'
    
    s=''.join(list_task)

    

    task_pep[message.chat.id]=correct_answer
    await bot.send_message(message.chat.id,text=f'Укажите варианты ответов, в которых верно выделена буква, обозначающая ударный гласный звук. Запишите номера ответов \n \n'+
                        f'{s} \n '+ 
                        
                        'Для того чтобы прекратить напишите /start')



@bot.message_handler(func=lambda message: '1' in message.text or '2' in message.text or '3' in message.text or '4' in message.text)
async def prov(message):
    znach=correct_task[message.chat.id]
    
    if task_pep[message.chat.id]==message.text:
        
        
        
        if znach=='':
            correct_task[message.chat.id]='1/1'

        else:
            correct_task[message.chat.id]=f'{int(znach[0])+1}/{int(znach[2])+1}'
            
        
        
        await bot.send_message(message.chat.id,text=f'Правильно!')
    else:
        
        if znach=='':
            correct_task[message.chat.id]='0/1'

        else:
            correct_task[message.chat.id]=f'{int(znach[0])}/{int(znach[2])+1}'
        await bot.send_message(message.chat.id,text=f'Не верно! Правильный ответ: {task_pep[message.chat.id]}')
    await task(message)


@bot.message_handler(commands=['start'])
async def start(message):
    
    global list_pepa


    correct_task.setdefault(message.chat.id,'')
    
    
    
    if message.chat.id not in slova_pep:
        
        slova_pep[message.chat.id]={}
    if f'{message.chat.id}' not in list_pepa:
        list_pepa.add(f'{message.chat.id} : @{message.chat.username }\n' if f'{message.chat.username}' !='None' else f'{message.chat.id} : {message.chat.first_name}\n')
    

    await bot.send_message(message.chat.id,text='Тренируй свою грамотность с этим ботом! ✍️📚 \nПроверяй знания орфоэпии и улучшай произношение сложных слов. 🔤🗣️\n\n Рекомендую подписаться на @orphoepi, чтобы быть в курсе всех новостей.\n\n Напиши /check и узнай свои результаты \n\n Новинка: Для того чтобы решать задания ЕГЭ напишите /task \n  \n Для того чтобы сбросить решенные слова напишите /clear',reply_markup=start_keyboard)






@bot.callback_query_handler(func=lambda callback:'run' in callback.data)
async def sort(callback):

    if callback.data in 'run':
        chs=random.randint(0,len(list_slov)-1)


        slova_pep[callback.message.chat.id][chs]=0



        word=list_slov[chs]

        rand=random.randint(0,1)
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




    chs=random.randint(0,len(list_slov)-1)
    while chs in slova_pep[callback.message.chat.id]:
        if len(slova_pep[callback.message.chat.id])==len(list_slov):

            await bot.send_message(callback.message.chat.id,text=f'Все слова прорешаны')

            await bot.send_message(callback.message.chat.id,text=f'Прорешаем слова в которых были ошибки?',reply_markup=repeat_keyboard)
            break

        chs=random.randint(0,len(list_slov)-1)

    if chs not in slova_pep[callback.message.chat.id]:


        slova_pep[callback.message.chat.id][chs]=0

        word=list_slov[chs]

        rand=random.randint(0,1)
        rand_2=1 if rand==0 else 0

        word_keyboard=types.InlineKeyboardMarkup()
        word_keyboard.row(
            types.InlineKeyboardButton(word[rand],callback_data=f'k{word[rand]} {word[0]} {chs}'),
            types.InlineKeyboardButton(word[rand_2],callback_data=f'k{word[rand_2]} {word[0]} {chs}')
        )
        await bot.send_message(callback.message.chat.id,text='Какое произношение правильное? 🤔🔠',reply_markup=word_keyboard)



@bot.callback_query_handler(func=lambda callback:'yes' in callback.data or 'no' in callback.data )
async def pepa(callback):

    if callback.data=='yes' or 'c' in callback.data:

        if callback.data=='yes':
            lsit_wrong=[]
            
            
            
            for i in slova_pep[callback.message.chat.id]:
                if slova_pep[callback.message.chat.id][i]==0:
                    lsit_wrong.append(i)
            
            list_wrong[callback.message.chat.id]=lsit_wrong
            

        
        
        if len(list_wrong[callback.message.chat.id])==0:
            await bot.send_message(callback.message.chat.id,text='Все слова правильно .\nДля того чтобы решать ещё раз напишите /clear')
        
        
    

        rand=random.randint(0,1)
        rand_2=1 if rand==0 else 0


        word=list_slov[ list_wrong[callback.message.chat.id][0] ]
        


        word_keyboard=types.InlineKeyboardMarkup()
        word_keyboard.row(
            types.InlineKeyboardButton(word[rand],callback_data=f'c{word[rand]} {word[0]}'),
            types.InlineKeyboardButton(word[rand_2],callback_data=f'c{word[rand_2]} {word[0]}')
        )
        await bot.send_message(callback.message.chat.id,text='Какое произношение правильное? 🤔🔠',reply_markup=word_keyboard)




    else:
        await bot.send_message(callback.message.chat.id,text='Для того чтобы начать заново напишите /clear')



@bot.callback_query_handler(func=lambda callback:'c' in callback.data)
async def corrections(callback):

    s=callback.data[1:]

    a=s.split(' ')
    

    
    if a[0]==a[1]:

        await bot.send_message(callback.message.chat.id,text='Верно!✅ Так держать! 💪✨')
        

        list_wrong[callback.message.chat.id]=list_wrong[callback.message.chat.id][1:]

        

        if len(list_wrong[callback.message.chat.id])==0:
            await bot.send_message(callback.message.chat.id,text='Все слова исправлены \n Для того чтобы решать ещё раз напишите /clear')
            
            slova_pep[callback.message.chat.id]={}

        else:

            await pepa(callback)


    else:

        await bot.send_message(callback.message.chat.id,text=f'Не правильно ❌ \nПравильное произношение: {a[1]} ✅')
        list_wrong[callback.message.chat.id]=list_wrong[callback.message.chat.id][1:]

        await pepa(callback)

import asyncio

asyncio.run(bot.polling(none_stop=True))
