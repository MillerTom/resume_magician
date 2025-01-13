import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { Button } from '@mui/material';

function ApplyJobPage({ name }) {
	const serverUrl = 'http://localhost:5000';

	const [isApplyPage, setIsApplyPage] = useState(false);
	const [records, setRecords] = useState([]);
	const [rows, setRows] = useState([]);
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(100);
  const [rowCount, setRowCount] = useState(0);

	const columns = [
		{ field: 'id', headerName: 'ID' },
		{ field: 'jobTitle', headerName: 'Job Title', },
		{ field: 'datePosted', headerName: 'Date Posted' },
		{
			field: 'resume',
			headerName: 'Resume',
			sortable: false,
			width: 300,
			renderCell: (params) => (
				<a href='params.row.resume'>{params.row.resume}</a>
			)
		},
		{
			field: 'action',
			headerName: 'Actions',
			sortable: false,
			width: 300,
			renderCell: (params) => (
				<>
					<Button>Apply For Job</Button>
					<Button color='error'>Reject Job</Button>
				</>
			)
		},
	];

	useEffect(() => {
		const token = localStorage.getItem('aToken');

		axios.post(`${serverUrl}/auth/get/records/`, {startPage: 0}, {
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			},
		})
		.then((response) => {
			const { records } = response.data;
			console.log(records);
      const start = page * pageSize;
      const end = start + pageSize;
      setRows(records.slice(start, end));
      setRowCount(records.length);
			setRecords(records);
		})
		.catch((error) => {
			console.log('---', error);
		})
	}, []);

  useEffect(() => {
		const start = page * pageSize;
		const end = start + pageSize;
		setRows(records.slice(start, end));
  }, [page, pageSize]);

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
					rows.length > 0 ? (
						<Paper sx={{ width: '100%' }}>
							<DataGrid
								rows={rows}
								columns={columns}
								sx={{ border: 0 }}
								pagination
								paginationMode="server"
								rowCount={rowCount}
								pageSize={pageSize}
								onPaginationModelChange = {(pageInfo) => {
									setPage(pageInfo.page);
									setPageSize(pageInfo.pageSize);
								}}
								rowsPerPageOptions={[10, 20, 50, 100]}
							/>
						</Paper>
					) : 'Loading...'
				): (<span>Homepage</span>)}
			</div>
    </div>
  );
}

export default ApplyJobPage;
