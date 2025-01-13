import './App.css';
import { Button } from '@mui/material';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CallBack from './CallBack';
import ApplyJobPage from './ApplyJobPage';
import { AZURE_AD_OAUTH2_KEY, AZURE_AD_OAUTH2_TENANT_ID, LOGIN_REDIRECT_URL, SERVER_URL } from './constants';

function App() {


  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

	useEffect(() => {
		const token = localStorage.getItem('aToken');
    if (token) {
      axios.get(`${SERVER_URL}/auth/get/user/`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
      })
      .then((response) => {
        const { name, email } = response.data;
        localStorage.setItem('aName', name);
        setName(name);
        setEmail(email);
        const pathname = window.location.pathname;
        if (!pathname.includes('applyjob'))
          window.location = '/applyjob';
      })
      .catch((error) => {
        setName('');
        console.log('---', error);
      });
    }
	}, []);

  return (
    <div style={{display: 'block'}}>
      <div style={{
        display: 'flex',
        width: '100%',
        height: '64px',
        alignItems: 'center',
        justifyContent: 'flex-end',
        backgroundColor: 'lightblue',
      }}>
        {!name ? (
          <Button onClick={() => {
            const params = {
              "client_id": AZURE_AD_OAUTH2_KEY,
              "response_type": "code",
              "redirect_uri": LOGIN_REDIRECT_URL,
              "scope": "openid profile email",
              "response_mode": "query",
            }
            const urlParams = new URLSearchParams(params).toString();
            const AZURE_AD_LOGIN_URL = `https://login.microsoftonline.com/${AZURE_AD_OAUTH2_TENANT_ID}/oauth2/v2.0/authorize?${urlParams}`;
            window.location = AZURE_AD_LOGIN_URL;
          }}>
            Login with Microsoft Account
          </Button>
        ) : (<span style={{color: 'black', fontWeight: 700, padding: '0px 24px'}}>{name}</span>)}
      </div>
      <div style={{ display: 'flex', width: '100%' }}>
        <Router>
          <Routes>
            <Route path='/callback' element={<CallBack setName={setName} />} />
            {name ? (<Route path='/applyjob' element={<ApplyJobPage name={name} email={email} />} />) : ''}
          </Routes>
        </Router>
      </div>
    </div>
  );
}

export default App;
