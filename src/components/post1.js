import React from 'react';
import {connect} from 'react-redux';
// import {Redirect} from 'react-router-dom';
import ReactChartkick, { LineChart, PieChart } from 'react-chartkick'
import Chart from 'chart.js'
import './post1.css';

ReactChartkick.addAdapter(Chart)

var data = [
	{"name":"Top-100", "data": {"1990": 107, "1991": 107, "1992": 107, "1993": 109, "1994": 111, 
								"1995": 109, "1996": 106, "1997": 112, "1998": 110, "1999": 111, 
								"2000": 109, "2001": 110, "2002": 105, "2003": 108, "2004": 109, 
								"2005": 109, "2006": 107, "2007": 109, "2008": 105, "2009": 107, 
								"2010": 107, "2011": 108, "2012": 111, "2013": 112 
								}
	},
	{"name":"Top-30", "data":  {"1990": 116, "1991": 114, "1992": 115, "1993": 115, "1994": 117, 
								"1995": 116, "1996": 116, "1997": 118, "1998": 113, "1999": 111, 
								"2000": 114, "2001": 114, "2002": 110, "2003": 116, "2004": 114, 
								"2005": 112, "2006": 112, "2007": 111, "2008": 111, "2009": 113, 
								"2010": 111, "2011": 113, "2012": 121, "2013": 133
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

				<LineChart data={data} min={100} max={140}/>
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