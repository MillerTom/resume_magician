import { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from '@mui/material';

function ApplyJobPage({ name, email }) {
	const serverUrl = 'http://localhost:5000';

	const token = localStorage.getItem('aToken');
	const [isApplyPage, setIsApplyPage] = useState(false);
	const [job, setJob] = useState({});
	const [jobIndex, setJobIndex] = useState(-1);
	const [isPendingApply, setIsPendingApply] = useState(false);
	const [startedAt, setStartedAt] = useState('');
	const [loading, setLoading] = useState(false);

	const getNewJob = () => {
		axios.post(`${serverUrl}/job/get/records/`, {startPage: 0}, {
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			},
		})
		.then((response) => {
			const { job } = response.data;
			setJob(job)
		})
		.catch((error) => {
			console.log('---', error);
		})
	}

	useEffect(() => {
		getNewJob();
	}, []);

  return (
    <div style={{display: 'flex', height: 'calc(100vh - 64px)'}}>
			<div style={{width: '240px', padding: '16px', borderRight: '1px solid lightblue'}}>
				<Button
					style={{width: '100%', justifyContent: 'flex-start', color: 'black'}}
					onClick={() => {setIsApplyPage(true);}}
				>
					Apply for Jobs
				</Button>
			</div>
			<div style={{width: 'calc(100vw - 308px)', padding: '16px'}}>
				{isApplyPage ? (
					Object.keys(job).length > 0 ? (
						<>
							<p style={{fontSize: '18px'}}><strong>Job Title:</strong> {job.jobTitle}</p>
							<p style={{fontSize: '18px'}}><strong>Date Posted:</strong> {job.datePosted}</p>
							<p style={{fontSize: '18px'}}><strong>Resume:</strong> <a href={job.resume}>{job.resume}</a></p>
							<div>
								<Button
									onClick={() => {
										if (!isPendingApply) {
											setIsPendingApply(true);
											setStartedAt((new Date()).toString());
											window.open(job.jobUrl, '_blank');
	
											axios.post(`${serverUrl}/job/start/`, {jobUrl: job.jobUrl, email}, {
												headers: {
													'Content-Type': 'application/json',
													'Authorization': `Bearer ${token}`
												},
											})
											.then((response) => {
												const { jobIndex } = response.data;
												console.log(jobIndex)
												setJobIndex(jobIndex);
											})
											.catch((error) => {
												console.log('---', error);
											})
										} else {
											setIsPendingApply(false);
											setJobIndex(-1);
											setLoading(true);
	
											axios.post(`${serverUrl}/job/applied/`, {
												jobIndex,
												email,
												jobUrl: job.jobUrl,
											}, {
												headers: {
													'Content-Type': 'application/json',
													'Authorization': `Bearer ${token}`
												},
											})
											.then((response) => {
												const _startedAt = new Date(startedAt);
												const finishedAt = new Date();
												const differenceInMs = finishedAt - _startedAt;
												const differenceInMinutes = (differenceInMs / (1000 * 60)).toFixed(1);
												alert(`It took ${differenceInMinutes} minutes to complete that job application.`);
												setJob({});
												getNewJob();
												setLoading(false);
											})
											.catch((error) => {
												console.log('---', error);
												setLoading(false);
											})
										}
									}}
									disabled={(isPendingApply && jobIndex < 0) || loading ? true : false}
								>
									{isPendingApply ? 'Finished applying' : 'Apply For Job'}
								</Button>
								&nbsp;
								&nbsp;
								<Button color='error'>Reject Job</Button>
							</div>
							{isPendingApply ? (
								<p style={{fontSize: '18px'}}>Job Apply Started At: {startedAt}</p>
							) : ''}
						</>
					) : 'Loading...'
				): (<span>Homepage</span>)}
			</div>
    </div>
  );
}

export default ApplyJobPage;