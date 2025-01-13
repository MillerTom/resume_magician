import { useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import { SERVER_URL } from './constants';


function CallBack({setName}) {
	const navigate = useNavigate();
	const [searchParams] = useSearchParams();
	const code = searchParams.get('code');

	useEffect(() => {
		if (code) {
			axios.post(`${SERVER_URL}/auth/get/token/`, { code })
			.then((res) => {
				const { access_token, id_token } = res.data;
				localStorage.setItem('aToken', access_token);
				localStorage.setItem('iToken', id_token);

				axios.get(`${SERVER_URL}/auth/get/user/`, {
          headers: {
            'Content-Type': 'application/json',
						'Authorization': `Bearer ${access_token}`
          },
        })
				.then((response) => {
					const { name } = response.data;
					setName(name);
					localStorage.setItem('aName', name);
					navigate('/applyjob');
				})
				.catch((error) => {
					console.log('---', error);
				});
			})
			.catch((err) => {
				console.log(err);
			});
		}
	}, [code]);

  return (
    <div style={{display: 'flex'}}>
      <h3 style={{marginLeft: '24px'}}>Please wait...</h3>
    </div>
  );
}

export default CallBack;
