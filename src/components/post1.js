import React from 'react';
import {connect} from 'react-redux';
// import {Redirect} from 'react-router-dom';
import ReactChartkick, { LineChart, PieChart } from 'react-chartkick'
import Chart from 'chart.js'
import './post1.css';

ReactChartkick.addAdapter(Chart)

var data = [
	{"name":"Top-100", "data": {"1990": 1.78, "1991": 1.78, "1992": 1.78, "1993": 1.82, "1994": 1.85, 
								"1995": 1.82, "1996": 1.77, "1997": 1.87, "1998": 1.83, "1999": 1.85, 
								"2000": 1.82, "2001": 1.83, "2002": 1.75, "2003": 1.8, "2004": 1.82, 
								"2005": 1.82, "2006": 1.78, "2007": 1.82, "2008": 1.75, "2009": 1.78, 
								"2010": 1.78, "2011": 1.8, "2012": 1.85, "2013": 1.87
								}
	},
	{"name":"Top-30", "data":  {"1990": 1.93, "1991": 1.9, "1992": 1.92, "1993": 1.92, "1994": 1.95, 
								"1995": 1.93, "1996": 1.93, "1997": 1.97, "1998": 1.88, "1999": 1.85, 
								"2000": 1.9, "2001": 1.9, "2002": 1.83, "2003": 1.93, "2004": 1.9, 
								"2005": 1.87, "2006": 1.87, "2007": 1.85, "2008": 1.85, "2009": 1.88, 
								"2010": 1.85, "2011": 1.88, "2012": 2.02, "2013": 2.22 
								}
	}
];

export class Post1 extends React.Component {
    render() {
        return (
        	<div className="article-full">
	        	<div className="article-full-title">
	        		<h1>{this.props.title}</h1>
	        	</div>
	        	<div className="article-full-date">
	        		<h4>{this.props.date}</h4>
	        	</div>
	        	<div className="article-full-body">
	        		Recently, it feels like movies are getting longer and longer. 
	        		But is that perception skewed towards a few outliers, or are films actually getting longer? 
	        		The answer is, as usual – complicated:<br/>
	        	</div>

				<LineChart data={data} />
				<div>
	        		<br/>
	        		Two interesting patterns emerge:<br/>
	        		First, the top-30 grossing movies are consistently longer than the top-100. That’s super interesting, 
	        		but we should not rush to the conclusion that longer equals more successful. The correlation 
	        		between runtime and domestic gross is actually very low for the top-100 (r-squared less than 0.1) – a fairly 
	        		odd result, which may imply that these blockbusters are unnecessarily long.<br/>
	        		Second, for 22 years – between 1990 and 2011 – movies’ runtimes were pretty much steady (less 
	        		than 6% fluctuations) for both the top-100 and the top-30. But then in 2012 and 2013 – the top-30 shot 
	        		up by about 15%, while the top-100 remained steady. Is this the beginning of a trend? We’ll have to wait 
	        		a couple of years to see about that.<br/>
	        		But let’s look at a histogram of all these 2,400 films:<br/>
	        		<br/>
	        		We see that this is not a pure bell-shaped Gaussian distribution: it is skewed to the right (the 
	        		average is beyond the peak). This means that when films get longer – they can get really long.<br/>
	        		But in any case, one thing is true: if you are like most Americans and primarily pay for tickets 
	        		for the top-30 biggest blockbusters – you are not wrong if you feel these films are getting longer. 
	        		But if you mix smaller films into your cinematic portfolio, that is not the case.<br/>
	        		So why are blockbusters getting longer? Perhaps the producers want to justify the ticket price by 
	        		providing the viewer with a long evening of cinematic entertainment – maybe even too long. Or perhaps 
	        		the huge upfront costs of setting up a blockbuster production make the marginal cost of an extra 30 
	        		minutes of film negligible? Or perhaps it’s the competition from premium television’s longer and more 
	        		complex story arcs?<br/>
	        		<br/>
	        		* All the raw runtime data is from boxofficemojo.com (100 films for each year; 2,400 films total. Yes – a Python script did that).

	        	</div>
	        </div>
        );
    }
}

const mapStateToProps = state => ({
    title: "Are Movies Really Getting Longer?", //state.title,
    date: "April 5, 2018" //state.date,
});

export default connect(mapStateToProps)(Post1);