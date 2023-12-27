// ChatroomSidebar.js
import React from 'react';

const ChatroomSidebar = () => {
  const tips = [
    { id: 1, title: '歡迎來到論證活動前導機器人' , content: '請透過聊天室來進行活動前導，先跟我說個`hi`來開始吧！' },
    // Add more rooms as needed
  ];
  
  return (
    <div className="sidebar">
      <h2>論證活動前導機器人</h2>
      <h2>論證活動題目：<p style={{color: '#aa3333'}}>請問核能發電是不是胎灣應該要發展的目標呢？</p></h2>
      <ul>
        {tips.map(tip => (
          <li>
            <div key={tip.id} >
              <p>{tip.title}</p>
              <p>{tip.content}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatroomSidebar;
