import telebot
import telegram
import time
import ast
import logging
from firebase import firebase
from datetime import date

#VARIABLES
types=telebot.types
today = str(date.today())
data={}
sd={'Score':0,'Correct':0,'Incorrect':0}
option=[]
expl={}
top_expl={}
topics=['CURRENT AFFAIRS','POLITY','INDIAN ECONOMY','ENVIRONMENT','HISTORY','GEOGRAPHY','SCIENCE AND TECHNOLOGY','DISASTER MANAGEMENT','SECURITY']
score={}
keyboard=types.InlineKeyboardMarkup()
eyeIcon = u"\U0001f440"
sadIcon = u"\U0001f614"
cupIcon = u"\U0001f3c6"
crossIcon = u"\u274E"
tickIcon = u"\u2705"
writeIcon = u"\u270F"
waitIcon = u"\u231B"
subIcon = u"\U0001f44d"
firebase = firebase.FirebaseApplication('<FIREBASE URL>', None)

bot_token='<BOT TOKEN>'

bot=telebot.TeleBot(token=bot_token,threaded=False)


#FUNCTIONS

def find(msg):
    for txt in msg:
        if 'Q' in txt:
            data['Question']=msg[2:]
            print(data)
            return msg[2:]
        elif 'O' in txt:
            data['opt'+msg[1]]=msg[3:]+'wrng'
            print(data)
            return msg[3:]
        elif 'A' in txt:
            data['opt'+msg[1]]=msg[3:]+'crct'
            print(data)
            return msg[3:]
        elif 'E' in txt:
            data['Explanation']=msg[2:]
            print(data)
            return msg[2:]

def strt_pg():

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text='Today\'s Question',
                                              callback_data='/quiz'))
    markup.add(types.InlineKeyboardButton(text='Old Questions',
                                              callback_data='old_topics'))
    return markup
        
def makekeyboard(strng):
    if 'op' in strng[0:2]:
        string1='rc'+strng
        string2='gr'+strng
    else:
        string1='kkcr'+strng
        string2='kkwr'+strng
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text='Correct',
                                              callback_data=string1),
        types.InlineKeyboardButton(text='Incorrect',
                                   callback_data=string2))

    return markup

def submit(q_no):
    if 'op' in q_no[0:2]:
        strng='op_sub'+q_no
    else:
        strng='SUBMIT'+q_no
    key = types.InlineKeyboardMarkup()

   
    key.add(types.InlineKeyboardButton("Submit",callback_data=strng))
    return key

def topic():
    top = types.InlineKeyboardMarkup()

   
    top.add(types.InlineKeyboardButton("CURRENT AFFAIRS",callback_data='cipot0'))
    top.add(types.InlineKeyboardButton("POLITY",callback_data='cipot1'))
    top.add(types.InlineKeyboardButton("INDIAN ECONOMY",callback_data='cipot2'))
    top.add(types.InlineKeyboardButton("ENVIRONMENT",callback_data='cipot3'))
    top.add(types.InlineKeyboardButton("HISTORY",callback_data='cipot4'))
    top.add(types.InlineKeyboardButton("GEOGRAPHY",callback_data='cipot5'))
    top.add(types.InlineKeyboardButton("SCIENCE AND TECHNOLOGY",callback_data='cipot6'))
    top.add(types.InlineKeyboardButton("DISASTER MANAGEMENT",callback_data='cipot7'))
    top.add(types.InlineKeyboardButton("SECURITY",callback_data='cipot8'))
    return top
    
def sel_top():
    top1 = types.InlineKeyboardMarkup()

   
    top1.add(types.InlineKeyboardButton("CURRENT AFFAIRS",callback_data='us_cipot0'))
    top1.add(types.InlineKeyboardButton("POLITY",callback_data='us_cipot1'))
    top1.add(types.InlineKeyboardButton("INDIAN ECONOMY",callback_data='us_cipot2'))
    top1.add(types.InlineKeyboardButton("ENVIRONMENT",callback_data='us_cipot3'))
    top1.add(types.InlineKeyboardButton("HISTORY",callback_data='us_cipot4'))
    top1.add(types.InlineKeyboardButton("GEOGRAPHY",callback_data='us_cipot5'))
    top1.add(types.InlineKeyboardButton("SCIENCE AND TECHNOLOGY",callback_data='us_cipot6'))
    top1.add(types.InlineKeyboardButton("DISASTER MANAGEMENT",callback_data='us_cipot7'))
    top1.add(types.InlineKeyboardButton("SECURITY",callback_data='us_cipot8'))
    return top1

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if str(message.chat.id) in expl :
        del expl[str(message.chat.id)]
    if str(message.chat.id) in top_expl:
        del top_expl[str(message.chat.id)]
    username=message.chat.first_name
    bot.send_message(message.chat.id,text="*    PARISHRAM IAS*\n\n"+'Welcome '+username+"\n\n*RULES*\n\nA Select the option "+writeIcon+"\nB Wait for option disable "+waitIcon+"\nC Submit once finish "+subIcon,
                     parse_mode=telegram.ParseMode.MARKDOWN_V2,reply_markup=strt_pg())

@bot.message_handler(commands=['create'])
def create_quiz(message):
    if data:
        firebase.post('/Quiz/'+today,data)
        bot.send_message(message.chat.id,text="*     Select the Topic*", 
                 parse_mode=telegram.ParseMode.MARKDOWN_V2,reply_markup=topic())
        
    else:
        bot.reply_to(message,'Create Question')

@bot.message_handler(commands=['del'])
def del_data(message):
    firebase.delete('/Quiz/','')
    bot.reply_to(message,'Deleted')


@bot.message_handler(func=lambda msg:msg.text is not None and 'Q ' in msg.text[0:2])
def quest(message):
    question=message.text
    question=find(question)
    bot.reply_to(message,'Options')


@bot.message_handler(func=lambda msg:msg.text is not None and 'O' in msg.text[0])
def opt(message):
    option=message.text
    option1=find(option)
    
        

@bot.message_handler(func=lambda msg:msg.text is not None and 'A' in msg.text[0])
def ans(message):
    answer=message.text
    answer1=find(answer)

@bot.message_handler(func=lambda msg:msg.text is not None and 'E ' in msg.text[0:2])
def exp(message):
    explain=message.text
    explain1=find(explain)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if(call.data.startswith("us_cipot")):
        index=int(call.data[-1])
        cid=call.message.chat.id
        result=firebase.get('/Topics/'+topics[index],'')
        if not result:
            bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Sorry!'+sadIcon+'Quiz Not Yet Created ',
                              message_id=call.message.message_id)
        else:
            l2_expl=[]
            qn=1
            for d1 in result:
                opt={}
                ind=0
                temp=result[d1]
                for d2 in temp:
                    if d2=='Explanation':
                        l2_expl.append(temp[d2])
                        top_expl[str(cid)]=l2_expl
                        print(top_expl)
                    elif d2=='Question':
                        print(qn)
                        participant=firebase.get('/Participants/'+str(cid)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn','')
                        if not participant:
                            firebase.post('/Participants/'+str(cid)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn',sd)
                        else:
                            for x in participant:
                                upd=x
                            firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+upd,'Score',0)
                            firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+upd,'Correct',0)
                            firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+upd,'Incorrect',0)
                                
                        qn=qn+1
                        ques=temp[d2]
                        if qn==2:
                            bot.edit_message_text(chat_id=call.message.chat.id,
                              text='*'+ques+'*',
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              message_id=call.message.message_id)
                        else:
                            bot.send_message(chat_id=call.message.chat.id,
                              text='*'+ques+'*',
                              parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    else:
                        ind=ind+1
                        opt[d2]=temp[d2]
                        option.append(temp[d2][:-4])
                        strng='op'+str(option.index(temp[d2][:-4]))+temp[d2][-4:]+str(qn-1)
                        print(strng+' '+str(call.message.chat.first_name))
                        print(option)
                        bot.send_message(cid,str(ind)+') '+temp[d2][:-4],reply_markup=makekeyboard(strng))
                bot.send_message(cid,'Submit your Answers',reply_markup=submit('op'+str(qn-1)))


    
    if(call.data.startswith("old_")):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="*     Select the Topic*", 
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              message_id=call.message.message_id,
                              reply_markup=sel_top())




    if(call.data.startswith("cipot")):
        index=int(call.data[-1])
        firebase.post('/Topics/'+topics[index],data);
        data.clear()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Question created Successfully '+subIcon,
                              message_id=call.message.message_id)

    if (call.data.startswith("rcop")):
        db=firebase.get('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn','')
        for x in db:
            score=db[x]['Score']
            correct=db[x]['Correct']
            wrong=db[x]['Incorrect']
        if 'crct' in call.data:
            score=score+1
            correct=correct+1
        else:
            score=score-1
            wrong=wrong+1
        print(f"call.data : {call.data} , type : {type(call.data)},"+str(score)+" "+str(correct)+" "+str(wrong))
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+x,'Score',score)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+x,'Correct',correct)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+x,'Incorrect',wrong)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=option[int(call.data[4])],
                              message_id=call.message.message_id)

    if (call.data.startswith("grop")):
        db=firebase.get('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn','')
        for x in db:
            score=db[x]['Score']
            correct=db[x]['Correct']
            wrong=db[x]['Incorrect']
        if 'wrng' in call.data:
            score=score+1
            correct=correct+1
        else:
            score=score-1
            wrong=wrong+1

        print(f"call.data : {call.data} , type : {type(call.data)},"+str(score)+" "+str(correct)+" "+str(wrong))
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+x,'Score',score)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+x,'Correct',correct)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn/'+x,'Incorrect',wrong)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=option[int(call.data[4])],
                              message_id=call.message.message_id)

    if (call.data.startswith("op_sub")):
        index=int(call.data[-1])-1
        db=firebase.get('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/old_qn','')
        for x in db:
            score=db[x]['Score']
            correct=db[x]['Correct']
            wrong=db[x]['Incorrect']
        lst=top_expl.get(str(call.message.chat.id))
        if not lst:
            string1='Sorry...Session Expired'
        else:
            string1="Your Score =  "+str(score)+" "+cupIcon+"\nCorrect = "+str(correct)+"  "+tickIcon+"\nWrong = "+str(wrong)+"  "+crossIcon+"\n*EXPLANATION*\n\n"+lst[index]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=string1,
                              message_id=call.message.message_id)


        
    if (call.data.startswith("kkcr")):
        db=firebase.get('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1]),'')
        for x in db:
            score=db[x]['Score']
            correct=db[x]['Correct']
            wrong=db[x]['Incorrect']
        if 'crct' in call.data:
            score=score+1
            correct=correct+1
        else:
            score=score-1
            wrong=wrong+1
        print(f"call.data : {call.data} , type : {type(call.data)},"+str(score)+" "+str(correct)+" "+str(wrong))
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1])+'/'+x,'Score',score)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1])+'/'+x,'Correct',correct)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1])+'/'+x,'Incorrect',wrong)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=option[int(call.data[4])],
                              message_id=call.message.message_id)

    if (call.data.startswith("kkwr")):
        db=firebase.get('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1]),'')
        for x in db:
            score=db[x]['Score']
            correct=db[x]['Correct']
            wrong=db[x]['Incorrect']
        if 'wrng' in call.data:
            score=score+1
            correct=correct+1
        else:
            score=score-1
            wrong=wrong+1

        print(f"call.data : {call.data} , type : {type(call.data)},"+str(score)+" "+str(correct)+" "+str(wrong))
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1])+'/'+x,'Score',score)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1])+'/'+x,'Correct',correct)
        firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1])+'/'+x,'Incorrect',wrong)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=option[int(call.data[4])],
                              message_id=call.message.message_id)

    if (call.data.startswith("SUBMIT")):
        index=int(call.data[-1])-1
        
        db=firebase.get('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(call.data[-1]),'')
        for x in db:
            score=db[x]['Score']
            correct=db[x]['Correct']
            wrong=db[x]['Incorrect']
        lst=expl.get(str(call.message.chat.id))
        if not lst:
            string1='Sorry...Session Expired'
        else:
            string1="Your Score =  "+str(score)+" "+cupIcon+"\nCorrect = "+str(correct)+"  "+tickIcon+"\nWrong = "+str(wrong)+"  "+crossIcon+"\n*EXPLANATION*\n\n"+lst[index]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=string1,
                              message_id=call.message.message_id)

    if(call.data.startswith("/quiz")):
        cid=call.message.chat.id
        result=firebase.get('/Quiz/'+today,'')
        if not result:
            bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Sorry!'+sadIcon+'Quiz Not Yet Created ',
                              message_id=call.message.message_id)
        else:
            l1_expl=[]
            qn=1
            for d1 in result:
                opt={}
                ind=0
                
                temp=result[d1]
                for d2 in temp:
                    if d2=='Explanation':
                        l1_expl.append(temp[d2])
                        expl[str(cid)]=l1_expl
                        print(expl)
                    elif d2=='Question':
                        print(qn)
                        participant=firebase.get('/Participants/'+str(cid)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(qn),'')
                        if not participant:
                            firebase.post('/Participants/'+str(cid)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(qn),sd)
                        else:
                            for x in participant:
                                upd=x
                            firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(qn)+'/'+upd,'Score',0)
                            firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(qn)+'/'+upd,'Correct',0)
                            firebase.put('/Participants/'+str(call.message.chat.id)+'/'+str(call.message.chat.first_name)+'/'+today+'/Q'+str(qn)+'/'+upd,'Incorrect',0)
                                
                        qn=qn+1
                        ques=temp[d2]
                        if qn==2:
                            bot.edit_message_text(chat_id=call.message.chat.id,
                              text='*'+ques+'*',
                              parse_mode=telegram.ParseMode.MARKDOWN_V2,
                              message_id=call.message.message_id)
                        else:
                            bot.send_message(chat_id=call.message.chat.id,
                              text='*'+ques+'*',
                              parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    else:
                        ind=ind+1
                        opt[d2]=temp[d2]
                        option.append(temp[d2][:-4])
                        strng=str(option.index(temp[d2][:-4]))+temp[d2][-4:]+str(qn-1)
                        print(strng+' '+str(call.message.chat.first_name))
                        print(option)
                        bot.send_message(cid,str(ind)+') '+temp[d2][:-4],reply_markup=makekeyboard(strng))
                bot.send_message(cid,'Submit your Answers',reply_markup=submit(str(qn-1)))
        

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)


