import { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, TextField } from '@mui/material';
import { SERVER_URL } from './constants';
import { formatDate } from './utils';

function ApplyJobPage({ name, email }) {
	const token = localStorage.getItem('aToken');
	const [isApplyPage, setIsApplyPage] = useState(false);
	const [backlog, setBacklog] = useState({});
	const [leaderboard, setLeaderboard] = useState([]);
	const [job, setJob] = useState({});
	const [jobIndex, setJobIndex] = useState(-1);
	const [isPendingApply, setIsPendingApply] = useState(false);
	const [startedAt, setStartedAt] = useState('');
	const [loading, setLoading] = useState(false);
	const [rejection, setRejection] = useState({isRejection: false, content: ''});
	const [jobDescripton, setJobDescription] = useState({isReadmore: true, content: ''});

	const getNewJob = () => {
		setJob({});
		axios.post(`${SERVER_URL}/job/get/records/`, {startPage: 0}, {
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			},
		})
		.then((response) => {
			const { job, backlog, leaderboard } = response.data;
			setJob(job);
			setJobDescription({isReadmore: jobDescripton.isReadmore, content: job.jobDescription});
			setBacklog(backlog);
			console.log(leaderboard);
			setLeaderboard(leaderboard);
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
					onClick={() => {setIsApplyPage(false);}}
				>
					LOG
				</Button>
				<Button
					style={{width: '100%', justifyContent: 'flex-start', color: 'black'}}
					onClick={() => {setIsApplyPage(true);}}
				>
					Apply for Jobs
				</Button>
			</div>
			<div style={{width: 'calc(100vw - 308px)', maxWidth: 'calc(100vw - 308px)', padding: '16px'}}>
				{isApplyPage ? (
					Object.keys(job).length > 0 ? (
						<>
							<p style={{fontSize: '18px'}}><strong>Job Title:</strong> {job.jobTitle}</p>
							<p style={{fontSize: '18px'}}><strong>Date Posted:</strong> {job.datePosted}</p>
							<p style={{fontSize: '18px'}}><strong>Job Description:</strong></p>
							<pre style={{fontSize: '16px', whiteSpace: 'pre-wrap'}}>
								{jobDescripton.isReadmore ? jobDescripton.content.slice(0, 500) : jobDescripton.content}
								<br />
								<span
									style={{color: 'blue', cursor: 'pointer', fontSize: '15px'}}
									onClick={() => {
										setJobDescription({isReadmore: !jobDescripton.isReadmore, content: jobDescripton.content});
									}}
								>
									{jobDescripton.isReadmore ? 'Read More' : 'Less'}
								</span>
							</pre>
							<p style={{whiteSpace: 'pre-wrap'}}>
								{/* <strong>Resume:</strong> <a style={{wordBreak: 'break-all'}} href={job.resume}>{job.resume}</a> */}
								<strong>Download Resume:</strong>&nbsp;
								<span
									style={{color: loading ? 'gray' : 'blue', cursor: 'pointer'}}
									onClick={() => {
										if (loading) return
										setLoading(true);
										axios.post(`${SERVER_URL}/job/download/resume/`, {resume: job.resume}, {
											headers: {
												'Content-Type': 'application/json',
												'Authorization': `Bearer ${token}`
											},
											responseType: 'blob',
										})
										.then((response) => {
											const url = window.URL.createObjectURL(new Blob([response.data]));
											const link = document.createElement('a');
											link.href = url;
											link.setAttribute('download', 'resume.docx');
											document.body.appendChild(link);
											link.click();
											setLoading(false);
										})
										.catch((error) => {
											console.log(error);
											setLoading(false);
										})
									}}
								>{job.resume}</span>
							</p>
							{rejection.isRejection ? (
								<TextField
									label="Reject Reason"
									variant="outlined"
									value={rejection.content}
									onChange={(e) => {setRejection({...rejection, content: e.target.value})}}
									fullWidth
									placeholder='Reject Reason'
									inputProps={{maxLength: 200}}
								/>
							) : ''}
							<div>
								<Button
									onClick={() => {
										if (!isPendingApply) {
											setIsPendingApply(true);
											setStartedAt((new Date()).toString());
											window.open(job.jobUrl, '_blank');
	
											axios.post(`${SERVER_URL}/job/start/`, {jobUrl: job.jobUrl, email}, {
												headers: {
													'Content-Type': 'application/json',
													'Authorization': `Bearer ${token}`
												},
											})
											.then((response) => {
												const { jobIndex } = response.data;
												setJobIndex(jobIndex);
											})
											.catch((error) => {
												console.log('---', error);
											})
										} else {
											setIsPendingApply(false);
											setLoading(true);
											console.log('jobIndex', jobIndex);
	
											axios.post(`${SERVER_URL}/job/applied/`, {
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
												getNewJob();
												setLoading(false);
												setJobIndex(-1);
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
								<Button color='error' onClick={() => {
									if (rejection.isRejection) {
										setLoading(true);
										axios.post(`${SERVER_URL}/job/reject/`, {jobUrl: job.jobUrl, rejectReason: rejection.content}, {
											headers: {
												'Content-Type': 'application/json',
												'Authorization': `Bearer ${token}`
											},
										})
										.then((response) => {
											console.log(response);
											getNewJob();
											setLoading(false);
										})
										.catch((error) => {
											console.log('---', error);
											setLoading(false);
										})
									}
									setRejection({...rejection, isRejection: !rejection.isRejection});
								}} disabled={loading}>
									{rejection.isRejection ? 'Finalize Rejection' : 'Reject Job'}
								</Button>
							</div>
							{isPendingApply ? (
								<p style={{fontSize: '18px'}}>Job Apply Started At: <strong>{formatDate(new Date(startedAt))}</strong></p>
							) : ''}
						</>
					) : 'Loading...'
				): (<div>
					<h3>BACKLOG METRICS</h3>
					{
						Object.keys(backlog).map(item => (
							<span style={{display: 'block'}}>{item} jobs not applied for: <strong>{backlog[item]}</strong></span>
						))
					}
					<h3>LEADERBOARD</h3>
					{
						leaderboard.map(item => (
							<span style={{display: 'block'}}>User {item.name.split(' ')[0]} has applied for <strong>{item.num_applied_jobs}</strong> jobs</span>
						))
					}
				</div>)}
			</div>
    </div>
  );
}

export default ApplyJobPage;