// ==UserScript==
// @name         WebSocket Hook Script with Selective JSON Processing
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Hook into existing WebSocket connections, selectively process JSON messages
// @author       Your Name
// @match        https://2023.holidayhackchallenge.com/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    var OriginalWebSocket = window.WebSocket;
    var webSockets = [];

    window.WebSocket = function(url, protocols) {
        var ws = protocols ? new OriginalWebSocket(url, protocols) : new OriginalWebSocket(url);
        webSockets.push(ws);

ws.addEventListener('message', function(event) {
    // Check if the message might be valid JSON (e.g., starts with '{' after removing two characters)
    if (event.data.slice(2).trim().startsWith('{')) {
        try {
            // Remove the first two characters and parse the rest as JSON
            var jsonData = JSON.parse(event.data.slice(2));
            console.log('Raw message data:', event.data);
            // Check for "onTheLine": "*" in the JSON data
            if (event.data.slice(2).includes("onTheLine")) {
                console.log('Special Condition Met:', event.data);
                sendMessage('reel');
            }

        } catch (e) {
            console.error('Error processing JSON message:', e);
        }
    } else {
        // If not JSON, you can log or ignore these messages
    }
});

        return ws;
    };

    for (var prop in OriginalWebSocket) {
        if (OriginalWebSocket.hasOwnProperty(prop)) {
            window.WebSocket[prop] = OriginalWebSocket[prop];
        }
    }

    function sendMessage(message) {
        if (webSockets.length > 0 && webSockets[0].readyState === WebSocket.OPEN) {
            webSockets[0].send(message);
        } else {
            console.error('No active WebSocket connection found.');
        }
    }

    setTimeout(function() {
        sendMessage('cast');
    }, 5000);

})();
