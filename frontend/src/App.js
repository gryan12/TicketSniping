// frontend/src/App.js

import React from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import ninja from "./images/ninja.png";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.css';		 // add this
import './App.css';
import 'react-dates/initialize';
import { DateRangePicker, SingleDatePicker, DayPickerRangeController } from 'react-dates';
import 'react-dates/lib/css/_datepicker.css';
import Email from 'react-email-autocomplete';
import {Sparklines, SparklinesLine} from 'react-sparklines';

import Select from 'react-select';
import LoadingOverlay from 'react-loading-overlay';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
};

function labelise(list){
	var arr=[];
	var i;
	for (i = 0; i < list.length; i++) {
		arr.push({value: list[i], label: formatPlayTheatre(list[i])})
	}
	return arr
};

function formatDate(string){
	var options = {year: 'numeric', month: 'long', day:'numeric', hour: "2-digit", minute: "2-digit", second: "2-digit"};
	return new Date(string).toLocaleDateString([],options);
}

function formatPlayTheatre(string){
	var splitStr = string.toLowerCase().split('-');
	for (var i = 0; i < splitStr.length; i++) {
		splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
	}
	return splitStr.join(' ');
}

function dynamic_play(play_dict, place){
	var output_list = []
	if (place == null){
		output_list=[]
	}else{
		output_list = play_dict[0][place["value"]]
	}
	if (output_list == undefined || output_list.length == 0){
		console.log("NULL PLAYS")
	//	output_list = play_dict[0]['All']
		output_list = []
	}
	return output_list;
}

function dynamic_section(play_section_dict, place, play){
	var output_list = []
	if (place == null || play == null){
		output_list=[]
	}else{
		console.log(play["value"])
		output_list = play_section_dict[0][place["value"]][play["value"]]
	}
	if (output_list == undefined || output_list.length == 0){
		console.log("NULL SECTIONS")
	//	output_list = play_dict[0]['All']
		output_list = []
	}
	return output_list;
}
const customDomains = ['gmail.com', 'hotmail.com', 'hotmail.co.uk', 'yahoo.com']
const sections= [
  { value: 'Stalls', label: 'Stalls' },
  { value: 'Balcony', label: 'Balcony' },
  { value: 'Circle', label: 'Circle' },
];

const highPrices= [
  { value: '20', label: '20' },
  { value: '30', label: '30' },
  { value: '40', label: '40' },
  { value: '50', label: '50' },
  { value: '75', label: '75' },
  { value: '100', label: '100' },
  { value: '150', label: '150' },
  { value: '200', label: '200' },
  { value: '9999', label: '200+' },
];

const noTicketsSelection= [
  { value: '1', label: '1' },
  { value: '2', label: '2' },
  { value: '3', label: '3' },
  { value: '4', label: '4' },
  { value: '5', label: '5' },
  { value: '99', label: '5+' },
];

const eveningOrMatinee= [
  { value: 'Any', label: 'Any' },
  { value: 'Evening', label: 'Evening' },
  { value: 'Matinee', label: 'Matinee' },
];
class App extends React.Component {

  state = {
	errorModalShow:false,
	loading:false,
	startDate:null,
	endDate: null,
	place: null,
	seatRow:null,
	seatCol:null,
	highPrice:null,
	section:null,
	play:null,
	noTickets:null,
	eveOrMat:null,
	date: [new Date(), new Date()],

	places: [],
	plays: [],
	sections:[],

	resultsModalShow:false,
	resultsReceived:false,
	results:[]


  };


  async handleSubmit() {
	console.log(this.state)
	 if ((this.state.startDate==null)||(this.state.endDate==null)||(this.state.place==null)||
		 (this.state.highPrice==null)|| (this.state.section==null)){
			this.setState({errorModalShow:true})
	 }else{
		this.setState({loading : true});
		axios.defaults.xsrfHeaderName = "X-CSRFToken";
		axios.defaults.withCredentials = true
		axios.defaults.xsrfCookieName = "csrftoken";

		let axiosConfig = {
		  headers: {
			  'Content-Type': 'application/json;charset=UTF-8',
			  'withCredentials':'true',
			  "Access-Control-Allow-Credentials": "true",
			  "Access-Control-Allow-Origin": "http://tik.ninja/",
			  "Access-Control-Allow-Methods":" GET, POST, OPTIONS, PUT, DELETE",
			  "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers",
		  }
		}

		let data = JSON.stringify({
			startDate: this.state.startDate.toISOString(),
			endDate: this.state.endDate.toISOString(),
			play: this.state.play.value,
			place: this.state.place.value,
			highPrice: this.state.highPrice.value,
			section: this.state.section.value,
			eveOrMat:this.state.eveOrMat.value,
			noTickets:this.state.noTickets.value,
		})
		const response = await axios.post('http://tik.ninja:8000/formSearch/', data, axiosConfig);
		const returned_data = await response.data;
		this.setState({results:returned_data})
		this.setState({resultsReceived: true})
		this.setState({resultsModalShow:true});
		}
	 }

  componentDidMount(){
	this.refreshTheatres();
	this.refreshPlays();
	this.refreshSections();
  }
  refreshTheatres= () => {
	axios
		.get("http://tik.ninja:8000/api/theatres/")
		.then(res => this.setState({ places: labelise(res.data) }))
  };
  refreshPlays= () => {
	axios
		.get("http://tik.ninja:8000/api/play/")
		.then(res => this.setState({plays: labelise(dynamic_play(res.data, this.state.place)) }))
  };
  refreshSections= () => {
	axios
		.get("http://tik.ninja:8000/api/section/")
		.then(res => this.setState({sections: labelise(dynamic_section(res.data, this.state.place, this.state.play)) }))
  };

  onDateSelect = option =>{
	this.setState({
		dates : option
	});
	console.log(this.state)
	};

  handleChangeLocation = option => {
	this.setState({ 
		place: option,
		play:null,
		section:null,
		highPrice: null,
	});
	this.refreshPlays();
	this.refreshSections();


  };

  handleChangePlay= option => {
	this.setState({ 
		play: option,
		section:null,
		highPrice: null,
	});
	this.refreshSections();
  };

  handleChangeSection= option => {
	this.setState({ 
		section: option,
		highPrice: null,
	});
  };

  handleChangeHighPrice= option => {
	this.setState({ 
		highPrice: option,
	});
  };

  handleChangeDropdown = selectedOption => {
	this.setState({ selectedOption });
	console.log(`Option selected:`, selectedOption);
  };

  handleChangeStartDate = date => {
	this.setState({
	  startDate: date,
	});
  };

  handleChangeEndDate = date => {
	this.setState({
	  endDate: date,
	});
  }
  handleChangeNoTickets= option => {
	this.setState({
	 noTickets : option,
	});
  }
  handleChangeEveOrMat= option => {
	this.setState({
	 eveOrMat: option,
	});
  }
  handleErrorModalClick = () => {
	this.setState({errorModalShow:false,})
  }
  handleResultsModalClick = () => {
	this.setState({loading : false})
	this.setState({resultsModalShow:false,});
	this.setState({resultsReceived:false,});
	if (document.getElementById("email-success")!==null && document.getElementById("email-failure")!==null){
		document.getElementById("email-success").style.display="none";
		document.getElementById("email-failure").style.display="none";
	}
  }
  handleEmailSubmit= () => {
	var email = document.getElementById("email-alert").value
	console.log(email);
	if (!(email.includes("@") || email.includes(".") || email != "" )){
		document.getElementById("email-failure").style.display="block";
		return
	}
	
	axios.defaults.xsrfHeaderName = "X-CSRFToken";
	axios.defaults.withCredentials = true
	axios.defaults.xsrfCookieName = "csrftoken";

	let axiosConfig = {
	  headers: {
		  'Content-Type': 'application/json;charset=UTF-8',
		  'withCredentials':'true',
		  "Access-Control-Allow-Credentials": "true",
		  "Access-Control-Allow-Origin": "http://tik.ninja/",
		  "Access-Control-Allow-Methods":" GET, POST, OPTIONS, PUT, DELETE",
		  "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers",
	  }
	}

	let data = JSON.stringify({
		email: document.getElementById("email-alert").value,
		startDate: this.state.startDate.toISOString(),
		endDate: this.state.endDate.toISOString(),
		play: this.state.play.value,
		place: this.state.place.value,
		highPrice: this.state.highPrice.value,
		section: this.state.section.value,
		eveOrMat:this.state.eveOrMat,
		noTickets:this.state.noTickets,

	})
	axios.post('http://tik.ninja:8000/emailAlert/', data, axiosConfig)
	.then(res =>  console.log(res.data[0]["success"]));
	document.getElementById("email-success").style.display="block";
	}

  handleResultsRender= () => {
	console.log(this.state.resultsReceived);
	sleep(3000);
	if (this.state.resultsReceived){
		this.setState({resultsReceived: false})
	}
  }

  renderResults = () => {
	const newItems = this.state.results.sort((a,b) => a.price - b.price);
	return newItems.map(item => (
			<a href={item.url}>
				<a href={item.url}>
					<li className="result-item">
							<div className="d-flex w-100 justify-content-between">
								<h5 className="mb-1">£{item.price.toFixed(2)}</h5>
								<small>{formatPlayTheatre(item.theatre_name)}</small>
								<small>{item.section} - {item.seat_row}{item.seat_col}</small>
							</div>
						<p className="mb-1">{formatPlayTheatre(item.play_name)} </p>
						<p className="mb-1">{formatDate(item.play_date_time)} </p>
						<small>{item.vendor.toUpperCase()}</small>
						<br></br>
						<br></br>
						<br></br>
					</li>
				</a>
			</a>
	));
  };
  renderSuggestions= () => {
	console.log(this.state.results[1].diff_date_prices)
	return (
		<div>	
			{this.state.results[1].diff_date_prices.length > 0 &&
			<p>Below are the earliest possible dates that the seat you queried is available at the moment:</p>
			}
			{this.state.results[1].diff_date_prices.map((item) => (
				<a href={item.url}>
					<li className="result-item">
							<div className="d-flex w-100 justify-content-between">
								<h5 className="mb-1">£{item.price.toFixed(2)}</h5>
								<small>{formatPlayTheatre(item.theatre_name)}</small>
								<small>{item.section} - {item.seat_row}{item.seat_col}</small>
							</div>
						<p className="mb-1">{formatPlayTheatre(item.play_name)} </p>
						<p className="mb-1">{formatDate(item.play_date_time)} </p>
						<small>{item.vendor.toUpperCase()}</small>
						<br></br>
						<br></br>
						<br></br>
					</li>
				</a>
			))}
		</div>
	);
  };
  renderResultsModal = () => {
	if (this.state.resultsModalShow == false) {
		return null;
	}else if (this.state.results[0] == 0){
		return(<Modal
		  show={this.state.resultsModalShow}
		  size="lg"
		  scrollable
		  aria-labelledby="contained-modal-title-vcenter"
		  centered
		  >
			<Modal.Header closeButton onClick={this.handleResultsModalClick}>
				<Modal.Title id="contained-modal-title-vcenter">
				Unfortunately, No tickets of that type were found. 
				</Modal.Title>
			</Modal.Header>
			<Modal.Body>
			<p>Would you like to set up an email alert? <br></br></p>
			<br></br>
			<div className="form-group">
				<label htmlFor="eac-input">Email address:-</label>
				<Email id="email-alert" className="form-control" placeholder="Enter email" domains={customDomains}/>
			</div>
			<div id ="email-failure">
				<br></br>
					<strong>Email Invalid</strong><br></br>
				<br></br>
			</div>
			<div id ="email-success">
				<br></br>
					<strong>Email submitted succesfully</strong><br></br>
					<strong>Alert for:-</strong><br></br>
					<p>lower date - {this.state.startDate.toISOString()}</p>
					<p>higher date - {this.state.endDate.toISOString()}</p>
					<p>play - {this.state.play.value}</p>
					<p>in location- {this.state.place.value}</p>
					<p>below price - {this.state.highPrice.value}</p>
					<p>in section - {this.state.section.value}</p>
				<br></br>
			</div>
			<br></br>
			<Button className="submit-btn" onClick={this.handleEmailSubmit}>Submit</Button>
			<br></br>
			<br></br>
			<div className = "covid-disclaimer"><p className="covid-disclaimer"><small>(Please Bear in mind COVID-19 means that there are limited tickets on sale until the late summer)</small></p></div>
			<ul className="list-unstyled">
				{this.renderSuggestions()}
			</ul>
			</Modal.Body>
			<Modal.Footer>
			<Button className="submit-btn" onClick={this.handleResultsModalClick}>Close</Button>
			</Modal.Footer>
		</Modal>
		)
	
	}else{
	console.log("full render, ");
	console.log(this.state.results.length);
	return (
		<Modal
		  show={this.state.resultsModalShow}
		  size="lg"
		  scrollable
		  aria-labelledby="contained-modal-title-vcenter"
		  centered
		  >
			<Modal.Header closeButton onClick={this.handleResultsModalClick}>
				<Modal.Title id="contained-modal-title-vcenter">
					Success! {this.state.results.length} tickets have been found!
				</Modal.Title>
			</Modal.Header>
			<Modal.Body>
				<ul className="list-unstyled">
					{this.renderResults()}
				</ul>
			</Modal.Body>
			<Modal.Footer>
				<Button className="submit-btn" onClick={this.handleResultsModalClick}>Close</Button>
			</Modal.Footer>
		</Modal>
	)
	}
	}


  render() {
	return (
	<LoadingOverlay
	  active={this.state.loading}
	  spinner
	  text='Loading...'
	  >

	  <div className="container">

		<Modal
		  show={this.state.errorModalShow}
		  size="lg"
		  aria-labelledby="contained-modal-title-vcenter"
		  centered
		  >
			<Modal.Header closeButton onClick={this.handleErrorModalClick}>
				<Modal.Title id="contained-modal-title-vcenter">
					Missing Information
				</Modal.Title>
			</Modal.Header>
			<Modal.Body>
				<p>
					There is not enough inputted information to return any shows.
				</p>
			</Modal.Body>
			<Modal.Footer>
				<Button className="submit-btn" onClick={this.handleErrorModalClick}>Close</Button>
			</Modal.Footer>
		</Modal>

		{this.renderResultsModal()}

		<h1 className= "Title">TiK NiNJA</h1>
		<div className="ninja">
			<img src={ninja} width="100" height="50" />
		</div>

			<div className="form-div">
					 <Select className="dropdown"
					value={this.state.place}
					onClick={this.toggleDatePicker}
					onChange={this.handleChangeLocation}
					options={this.state.places} placeholder={"Location"}
					isSearchable={false}
					/>
					 <Select className="dropdown"
					value={this.state.play}
					onChange={this.handleChangePlay}
					options={this.state.plays} placeholder={"Play"}
					isSearchable={false}
					/>


					 <Select className="dropdown"
					value={this.state.section}
					onChange={this.handleChangeSection}
					options={this.state.sections} placeholder={"Section"}
					isSearchable={false}
					/>
					 <Select className="dropdown"
					value={this.state.highPrice}
					onChange={this.handleChangeHighPrice}
					options={highPrices} placeholder={"Max Price"}
					isSearchable={false}
					/>
					 <Select className="dropdown"
					value={this.state.noTickets}
					onChange={this.handleChangeNoTickets}
					options={noTicketsSelection} placeholder={"Number of Tickets"}
					isSearchable={false}
					/>
					 <Select className="dropdown"
					value={this.state.eveOrMat}
					onChange={this.handleChangeEveOrMat}
					options={eveningOrMatinee} placeholder={"Evening Or Matinee"}
					isSearchable={false}
					/>
		   </div>
		   <h6 className="between">Between</h6>
			<div className="date-range" >
				<DateRangePicker
				 startDateId="startDate"
				 endDateId="endDate"
				 startDate={this.state.startDate}
				 endDate={this.state.endDate}
				 onDatesChange={({ startDate, endDate }) => { this.setState({ startDate, endDate })}}
				 focusedInput={this.state.focusedInput}
				 onFocusChange={(focusedInput) => { this.setState({ focusedInput })}}
				 withPortal={true}
				 minimumNights={0}
				/>
			</div>
		   <div className="submit-div">
				<Button className="submit-btn" onClick={(e) => this.handleSubmit(e)}>Submit</Button>
		   </div>

	  </div>
	  </LoadingOverlay>
	);
  }
}

export default App;
