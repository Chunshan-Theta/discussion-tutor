// App.js
import React, { useState } from 'react';
import './App.css';
import ChatroomSidebar from './ChatroomSidebar';
import Chatroom from './Chatroom';
import ChatInput from './ChatInput';

const App = () => {
  const [currentRoom, setCurrentRoom] = useState(1); // Example initial room ID
  const [messages, setMessages] = useState([]); // Placeholder for messages

  const rooms = [
    { id: 1, name: 'Room 1' },
    { id: 2, name: 'Room 2' },
    // Add more rooms as needed
  ];

  const changeRoom = roomId => {
    // Implement logic to fetch messages for the selected room
    // For example, an API call to get messages for the new room
    // Update the messages state accordingly
    setCurrentRoom(roomId);
    // Fetch and set messages for the new room
    // Example: fetchMessagesForRoom(roomId).then(messages => setMessages(messages));
  };

  const sendMessage = message => {
    // Implement logic to send a message to the current room
    // For example, an API call to send the message to the current room
    // Update the messages state accordingly
    const newMessage = { id: messages.length + 1, text: message, sender: 'Me' };
    const newMessageFromBot = { id: messages.length + 1, text: "I got", sender: 'Bot' };
    setMessages([...messages, newMessage, newMessageFromBot]);
    // Example: sendNewMessageToRoom(currentRoom, message).then(updatedMessages => setMessages(updatedMessages));
  };

  return (
    <div className="app">
      <ChatroomSidebar rooms={rooms} changeRoom={changeRoom} />
      <div className="main">
        <Chatroom messages={messages} />
        <ChatInput sendMessage={sendMessage} />
      </div>
    </div>
  );
};

export default App;
