( function($){

	var kc_buttons_fix = function() {

		$('div.btn-group[data-toggle=buttons-radio]').on('click','input[type=radio]',function(){
			if( this.checked == true) {

				var $btnGroup = $(this).parents('.btn-group');

				var $checkedRadios = $btnGroup.find('input[type="radio"]:checked');

				$checkedRadios.not($(this)).removeAttr('checked');
			}
		});


		//uncheck Alla automatically if others is checked
		$('div.btn-group[data-toggle=buttons-checkbox]').find('input[type="checkbox"]').not('[value="Alla"]').on('click',function(){
			if( $(this).prop('checked') ){
				$('label[for="subjectall"]').removeClass('active');
				$('input[type="checkbox"]#subjectall').prop('checked',false);
			}
		})

		//uncheck all others if Alla is checked
		$('div.btn-group[data-toggle=buttons-checkbox]').on('click','input[type=checkbox][value=Alla]',function(){
			var $targets = $(this).parents('.btn-group').find('input[type="checkbox"]:checked').not('[value="Alla"]');
			$targets.each(function(index,value){
				$id_of_checkbox = $(value).attr('id');
				$('label[for="'+$id_of_checkbox+'"]').removeClass('active');
				$(value).prop('checked',false);
			})
		});

		$('#time_ahead_filters').on('click','input[type=radio]',function(){

			var $me = $(this);

			var $archive_current_state = $('#archive_only_filters');
			if( $me.attr('value') == 'archive') {
				if( $archive_current_state.attr('data-display') != 'visible'){
					$archive_current_state.slideDown('fast',function(){
						$archive_current_state.attr('data-display','visible');
					})

				}
			}else{
				if( $archive_current_state.attr('data-display') == 'visible'){
					$archive_current_state.slideUp('fast',function(){
						$archive_current_state.attr('data-display','hidden');

						//$('input[type="radio"][name="event_tags"]').attr('checked',false);

						//$('input[type="radio"][name="event_tags"][value="event_tags_all"]').prop('checked',false);

					})

				}
			}
		});//

		//show advanced options condition
		$('#toggle_advanced_search').click(function(e){
			$('input[name="advanced_search"]').val(function(i,v){
				return (v==0)?1:0;
			});
			$(this).toggleClass('btn-advanced');
			$('#advanced_filters').slideToggle('fast');
			e.preventDefault();
		})

		//round border fix
		$('#eventSearchForm').find('.btn-group').each(function(){
			$(this).find('label').last().addClass('btn-last');
		})

		$('#time_ahead_filters').find('label').eq(-2).addClass('second-last');
		$('#time_ahead_filters').find('label').eq(-1).addClass('last');



	}




	var calendar_search = function() {


		var $searchForm 				= $('form#eventSearchForm'),
			$searchLoader 				= $('#searchloader'),
			$search_found_results		= $('#search_found_results'),
			$advanced_filters_column1  	= $('#advanced_filters_column1'),
			$normal_day_filter 			= $('#time_ahead_filters'),
			$custom_day_filter 			= $('#custom_day_till_filter'),
			$freeTextSearchField 		= $('input#freetextsearch' )
		;


		/******************************************************************************************
		 * major form submit procedures
		 **************************************/
		var kcPjaxOptions = {
			scrollTo	: false,
			timeout: null,
			error: function(xhr,err){
				alert('Something went wrong: ' + err);
			}
		}
		var magicPjxySearch = function (event){
			console.log($searchForm.serialize());
			//console.log($custom_day_filter.find('input[type=radio]').is('checked'));
			//return false;
 			$.pjax.submit(event, '#eResults',kcPjaxOptions)
		};

		$(document).on('submit', 'form#eventSearchForm',magicPjxySearch );

		$(document).on('pjax:beforeSend', function(a,b) {
			$search_found_results.hide();
		 	$searchLoader.show();
		});

		$(document).on('pjax:complete', function() {
			$('#show_next_events').attr('data-offset',0);
				jQuery(this).find('div.calendar-search-list:first').addClass('first-result');
				extraSidebarFix(true);
				$searchLoader.hide();
				$(document).trigger('kcStockholm.eventListUpdated');
		});
		$(document).on('pjax:success', function(data, status, xhr) {
			$countTotal=$('#search-total').data('total');
			$countTotal = $countTotal>0 ? $countTotal : '0';
			$('#search_found_results span').html($countTotal);
			$search_found_results.show();

		});

		///////////////////////////////////////////////////////////////////////////////////////


		/************************************************************************************************
		* also submit form on these events
		**/
		$searchForm.find('.form-devider input[type="radio"] ,.form-devider input[type="checkbox"]').click(function(event){
			//synchronize mobile values too
			$('.form-devider select',$searchForm).attr('disabled','disabled');
			$searchForm.submit();
		});
		$searchForm.find('.form-devider select').change(function(){
			//synchronize mobile values too
			$('.form-devider input[type="radio"] ,.form-devider input[type="checkbox"]',$searchForm).attr('disabled','disabled')
			$searchForm.submit();
		});

		$advanced_filters_column1.find('select').change(function(){$searchForm.submit();})

		$('.btn-favorite').click( function(e){
			e.preventDefault();
			var $me = $(this);
			$me.toggleClass('active');
			$('input[name="fav"]',$('#eventSearchForm')).val(function(){
				return ($me.hasClass('active'))?1:0;
			});
			$searchForm.submit();

		})


		///////////////////////////////////////////////////////////////////////////////////////


		/***************************************************************************************
		* custom requiested actions
		****************************************************************************************/
		//when row 1 filter days is selected , filters in column 2 should be reset and vice versa
		$normal_day_filter.find('input').click(function(){
			$('select#custom_day_till_filter option').prop('selected',false).eq(0).prop('selected',true);
			$('#event_calendar_date_search').datepicker('update',$('#event_calendar_date_search').attr('data-date'));
			$('.selectpicker').selectpicker('refresh');
		});

		var adjust_day_filters_change = function (){
			if( $("option:selected", $custom_day_filter).val() != 'Alla'){
				//console.log('here');
				/*$('input',$normal_day_filter).prop('checked',false);*/
				//$normal_day_filter.find('input').eq(0).trigger('click');
				$normal_day_filter.find('input').eq(0).prop('checked',true );
				$normal_day_filter.find('input').eq(0).prop('checked',false );

				$('input',$normal_day_filter).removeAttr('checked');
				$normal_day_filter.val('');

				$('label',$normal_day_filter).removeClass('active');

				var $archive_current_state = $('#archive_only_filters');
				if( $archive_current_state.attr('data-display') == 'visible'){
					$archive_current_state.slideUp('fast',function(){
						$archive_current_state.attr('data-display','hidden');
					});
					$('input',$archive_current_state).prop('checked',false);
					$('label',$archive_current_state).removeClass('active');
				}

			}else{
				//make 7 days clicked again
				$normal_day_filter.find('input').eq(2).prop('checked',true );
				$('label',$normal_day_filter).eq(2).addClass('active');
				$freeTextSearchField.val('');

			}
		};


		$custom_day_filter.on('change',adjust_day_filters_change );
		$('#event_calendar_date_search').on('click',adjust_day_filters_change);
		// $freeTextSearchField.on('focus',function(i,v){
		// 	if( $custom_day_filter.val()  == 'Alla' ){
		// 		$custom_day_filter.val('7');
		// 		$('.selectpicker').selectpicker('refresh');
		// 	}
		// 	adjust_day_filters_change();
		// });

		$freeTextSearchField.keypress(function(evt){
			var code = (evt.keyCode ? evt.keyCode : evt.which);
			if (code==13){
				$searchForm.submit();
				evt.preventDefault();
			}

		});


		/*
			$custom_day_filter.on('change',function(){

				if( $("option:selected", this).val() != 'Alla'){


					//$normal_day_filter.find('input').eq(0).trigger('click');
					$normal_day_filter.find('input').eq(0).prop('checked',true );
					$normal_day_filter.find('input').eq(0).prop('checked',false );

					$('input',$normal_day_filter).removeAttr('checked');
					$normal_day_filter.val('');

					$('label',$normal_day_filter).removeClass('active');

					var $archive_current_state = $('#archive_only_filters');
					if( $archive_current_state.attr('data-display') == 'visible'){
						$archive_current_state.slideUp('fast',function(){
							$archive_current_state.attr('data-display','hidden');
						});
						$('input',$archive_current_state).prop('checked',false);
						$('label',$archive_current_state).removeClass('active');
					}

				}else{
					//make 7 days clicked again
					$normal_day_filter.find('input').eq(2).prop('checked',true );
					$('label',$normal_day_filter).eq(2).addClass('active');

				}
			});
		*/


		/***************************************************************************************
		* reset button action
		****************************************************************************************/
		$('#reset_search_form').click( function(e){


			$searchForm[0].reset();

			$('.selectpicker option').prop('selected',false).eq(0).prop('selected',true);
			var $fav_btn = $('a.btn-favorite',$searchForm);
			if( $fav_btn.hasClass('active') ){

				$fav_btn.removeClass('active');
				$('input[name=fav]',$searchForm).val(0);

			}

			var $subjectFilters = $('#subject_option_filters');

			//$('#subject_option_filters').button('reset');



			//uncheck all
			$twoRowscontext = $subjectFilters.add($normal_day_filter);

			$('label',$twoRowscontext).removeClass('active');
			$('input',$twoRowscontext).prop('checked',false);
			//check ALLA in particular
			$('label[for="subjectall"]',$subjectFilters).addClass('active');
			$('input[type="checkbox"]#subjectall',$subjectFilters).prop('checked',true);

			$normal_day_filter.find($('label')).eq(2).addClass('active');
			$normal_day_filter.find($('input')).eq(2).prop('checked',true);



			//$('.selectpicker').selectpicker('render');
			$('.selectpicker').selectpicker('refresh');
			//console.log('resetted?');
			//$normal_day_filter.button('reset');
			//$('#subject_option_filters').button('reset');
			e.preventDefault();
			return false;
		});



		//for debugging
		//==========================================================================
		/*
			$(document).on('pjax:send', function() {
			  //$('#loading').show();
			  console.log('pjax loading');

			})

			$(document).on('pjax:timeout', function(event) {
			  // Prevent default timeout redirection behavior
			  event.preventDefault()
			})

			$(document).on('pjax:complete', function() {
			  //$('#loading').hide()
			  console.log('pjax complete');
			})
			var customEventList = ['pjax:beforeSend', 'pjax:send', 'pjax:complete', 'pjax:success', 'pjax:error ', 'pjax:timeout'];

			customEventList.forEach(function(customEvents) {

				$(document).on(customEvents, function() {
					console.log(customEvents+ ' event fired');
				});

			});
		*/

		//==========================================================================
	}

	var	calendar_search_datepicker = function(){
		/**
		 * Swedish translation for bootstrap-datepicker
		 * Patrik Ragnarsson <patrik@starkast.net>
		 */
		;(function($){
			$.fn.datepicker.dates['sv'] = {
				days: ["SÃ¶ndag", "MÃ¥ndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "LÃ¶rdag", "SÃ¶ndag"],
				daysShort: ["SÃ¶n", "MÃ¥n", "Tis", "Ons", "Tor", "Fre", "LÃ¶r", "SÃ¶n"],
				daysMin: ["SÃ¶", "MÃ¥", "Ti", "On", "To", "Fr", "LÃ¶", "SÃ¶"],
				months: ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December"],
				monthsShort: ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"],
				today: "I Dag"
			};
		}(jQuery));

		var $dateDiv 	= 	$('input#event_calendar_date_search.bootstrap_datepicker'),
			startDate 	=  	new Date( $dateDiv.attr('data-date') ),
			ref_date	=	$('#ref_date')
		;


		var $nativeDateField = $('input#event_calendar_date_search.native_datepicker');

		var $rangeSelector = $('#custom_day_till_filter');

		$nativeDateField.click(function(){
			if( $rangeSelector.val()  == 'Alla' ){
				$rangeSelector.val('7');
				$rangeSelector.selectpicker('refresh');
			}
		})

/*		$dateDiv.datepicker({
			language : 'sv'
			,todayBtn: 'linked'
		})*/
		var theDatepicker = $dateDiv.datepicker({
			language : 'sv'
			,todayBtn: 'linked'
		})
		.on('click',function(ev){

			//console.log($rangeSelector.val());
			if( $rangeSelector.val()  == 'Alla' ){
				$rangeSelector.val('7');
				$('.selectpicker').selectpicker('refresh');
			}


		})
		.on('changeDate',function(ev){
			ref_date.val($dateDiv.data('datepicker').getFormattedDate());
			theDatepicker.datepicker('hide');
			//console.log(ev);
			//console.log($dateDiv.data('datepicker'));
			//console.log(ev.date.valueOf());
			//console.log(startDate.valueOf());
			/*
			if (ev.date.valueOf() < startDate.valueOf()){ //date-start-display.valueOf()
				//console.log('less');
				//archive
			}else{
				//console.log('more');
				//regular
			}*/

		});




		/*
		if(  typeof($.mobiscroll) != 'undefined'){
			$('input[type=date],input.dateInput').mobiscroll().date({
		        theme: 'default',
		        display: 'modal',
		        dateOrder: 'mmD ddyy',
		        mode: 'clickpick'//scroller/clickpick/mixed
		    });
		}else{
			//console.log('mobiscroll not included');
		}*/
	}


	var calendar_pagination_old = function (e) {

		var	$searchLoaderBottom			= $('#searchloaderbottom');


		$(document).on('click', '#show_next_events', function(e){

			var dataOffset = parseInt($(this).attr('data-offset'))  ;



			var defaultKeyvalues = {};

			var currentUrl = document.location.href;
			if( currentUrl.indexOf('?')!= -1){
				var currentUrlQuery = currentUrl.substring(currentUrl.lastIndexOf("?")+1);
				if(currentUrlQuery !=''){
					var filtersQueries = currentUrlQuery.split("&");
					filtersQueries.forEach(function(aFilter){
						//console.log(aFilter.split("="));
						filterKey = aFilter.split("=")[0];
						filtervalue = aFilter.split('=')[1];

						defaultKeyvalues[filterKey] = filtervalue;
					})
					//console.log(defaultKeyvalues);
				}




			}





			defaultKeyvalues.action="paginated_next_events";
			defaultKeyvalues.offset=dataOffset;
			$searchLoaderBottom.show();
			jQuery.ajax({
						  url: abfStockholm.ajaxUrl,
						  type: 'GET',
						  //dataType: 'xml/html/script/json/jsonp',
						  data: defaultKeyvalues,
						  complete: function(xhr, textStatus) {
							$searchLoaderBottom.hide();
						  },
						  success: function(data, textStatus, xhr) {
						    //called when successful
						    						    //called when complete
						     //console.log(textStatus);
						     if( data.length>1){
							     $('#eResults').append(data).hide().fadeIn(1000,'easeOutExpo');
								  extraSidebarFix(true);
								  $('#show_next_events').attr('data-offset',dataOffset+1);


								  //document.location.hash = 'offset_'+dataOffset;


						     }

						  },
						  error: function(xhr, textStatus, errorThrown) {
						    //called when there is an error
						  }
						});


/*			jQuery.post(abfStockholm.ajaxUrl, defaultKeyvalues, function(data, textStatus, xhr) {
			  //optional stuff to do after success
			  console.log(textStatus);
			  $('#eResults').append(data);
			  $('#show_next_events').attr('data-offset',dataOffset);

			});*/


			//$.post(abfStockholm.ajaxUrl,)
			//console.log('ready to go');
			e.preventDefault();
		});
	};//end of calendar pagination

	var calendar_pagination = function (e) {

		var	$searchLoaderBottom		= $('#searchloaderbottom');
		var	$search_found_results		= $('#search_found_results');
		var $showMmoreButton		= $('#show_next_events');
		var dataOffset 				= parseInt($showMmoreButton.attr('data-offset'))  ;

		var defaultKeyvalues = {};

		var searchQuery = function(){
			var currentUrl = document.location.href;
			if( currentUrl.indexOf('?')!= -1){
				var currentUrlQuery = currentUrl.substring(currentUrl.lastIndexOf("?")+1);
				if(currentUrlQuery !=''){
					var filtersQueries = currentUrlQuery.split("&");
					//filtersQueries.forEach(function(aFilter){
					//using underscore function _.each for cross browser ie <=8 doesn't support foreEach
					_.each(filtersQueries,function(aFilter){	//filtersQueries.forEach(function(aFilter){

						//console.log(aFilter.split("="));
						filterKey = aFilter.split("=")[0];
						filtervalue = aFilter.split('=')[1];

						defaultKeyvalues[filterKey] = filtervalue;
					})
					//console.log(defaultKeyvalues);
				}
			}
		};

		defaultKeyvalues.action="paginated_next_events";

		var manualShowMore = function() {
			//console.log('currently used offset is '+ dataOffset );
			defaultKeyvalues.offset=dataOffset;
			$searchLoaderBottom.show();
			$search_found_results.hide();
			requestRunning = true;
			jQuery.ajax({
			  url: abfStockholm.ajaxUrl,
			  type: 'GET',
			  //dataType: 'xml/html/script/json/jsonp',
			  data: defaultKeyvalues,
			  complete: function(xhr, textStatus) {
				$searchLoaderBottom.hide();
				requestRunning = false;
			  },
			  success: function(data, textStatus, xhr) {
			     if( data.length>1){
			     		data = removeRedundantHeadings(data);
			     		//console.log(data);
		     			data = '<a name="offset_'+dataOffset+'"></a>'+data;

				     $('#eResults').append(data).hide().fadeIn(1000,'easeOutExpo');
					  extraSidebarFix(true);
					  $('#show_next_events').attr('data-offset',dataOffset+1);
					  //document.location.hash = 'offset_'+dataOffset;
					  $.sessionStorage.setItem('manualOffset', dataOffset+1);

					  $(document).trigger('kcStockholm.eventListUpdated');
					  $('#time_ahead_filters label').removeClass('active');
				}
			  },
			  error: function(xhr, textStatus, errorThrown) {}
			});
		};

		var requestRunning = false;
		$(document).on('click', '#show_next_events', function(e) {
			if (requestRunning) { // don't do anything if an AJAX request is pending
				return;
			}
			dataOffset = parseInt($showMmoreButton.attr('data-offset'))  ;
			//dataOffset++
			searchQuery();
			manualShowMore();
			e.preventDefault();
		});

		var autoShowMoreLoop = 0;
		var lastMaxOffset = $.sessionStorage.getItem('offset');

		var autoShowMore = function() {

			//console.log('auto offset:'+ autoShowMoreLoop );
			//console.log('max offset:'+ lastMaxOffset );

			defaultKeyvalues.offset=autoShowMoreLoop;

			if( autoShowMoreLoop < lastMaxOffset ){

				//console.log('currently used offset is '+ autoShowMoreLoop );
				$searchLoaderBottom.show();
				$.ajax({
				  url: abfStockholm.ajaxUrl,
				  type: 'GET',
				  async : true,
				  data: defaultKeyvalues,
				  complete: function(xhr, textStatus) {

					//console.log('autoShowmore loop  '+autoShowMoreLoop);
				  },
				  success: function(data, textStatus, xhr) {
				     if( data.length>1){
				     	autoShowMoreLoop++;
				     	++dataOffset;
				     	$('#show_next_events').attr('data-offset',dataOffset);
				     	//$('#eResults').append(data).hide().fadeIn(1000,'easeOutExpo');
						//extraSidebarFix(true);
						data = removeRedundantHeadings(data);

						data = '<a name="offset_'+(dataOffset-1)+'"></a>'+data;
						$('#eResults').append(data);
						autoShowMore();
						$(document).trigger('kcStockholm.eventListUpdated');

					}else{

					}
				  },
				  error: function(xhr, textStatus, errorThrown) {}
				});

			}else{
				$searchLoaderBottom.hide();
				$.sessionStorage.setItem('offset', 0);
				$.sessionStorage.setItem('manualOffset', 0);
				extraSidebarFix(true);

			}
		};


		/**
		 * This function is built in order to remove the same date heading when rendered after
		 * clicking "show more events" because server sends the events grouped by date each time a request is sent
		 *
		 * @param  subject  (html string ) This is the exact response by the server
		 *
		 * @return html Processed html in which the redundant heading ( if already exists ) is removed
		 *
		 */
		var removeRedundantHeadings = function(subject){

			var content  = jQuery('<div/>').html(subject);
			var headings = content.find('h2.published-date');
            if( headings.length > 0 ){

				//the possible redundant heading is always the first heading of the server respoinse
				//no need to check for the other events
				var headingToCheck = jQuery(headings[0]).text();

				// till this event this server response is not alreay appended to the actual dom
				// ie, it is still on the fly
				// here check if heading with the same text is already in the div #eResults
				var sameHeadingBefore = jQuery('h2:contains("'+headingToCheck+'")','#eResults');//.not().eq(0);

				//is there is remove it
				if( sameHeadingBefore.length > 0 ){
					jQuery(headings[0]).remove();
				}

		    }

			//return the html so that it can now be placed in the dom
			return content.html();

		}

		//the current function is already fired(executed) on document load

		$(document).on('kcStockholm.moreSearchResults',function(){
			//console.log('kcStockholm.moreSearchResults event fired ');
			if( lastMaxOffset > 0){
				//console.log('before autoShowmore ');
				searchQuery();
				$searchLoaderBottom.show();
				autoShowMore();
				//console.log('after autoShowmore ');
				extraSidebarFix(true);
				$searchLoaderBottom.hide();



				//call the autoload procedure
			}
			//no more calling the procedure until
			$(document).off('kcStockholm.moreSearchResults');
		});

		$(document).trigger('kcStockholm.moreSearchResults');

		//function to transfer manual offsets into real offsets that is checkid by kcStockholm.moreSearchResults event
		var attachRealOffset = function(e){
			//console.log('attachRealOffset called');
			//alert('called ahem!');
			var temp = $.sessionStorage.getItem('manualOffset');
			if ( temp > 0 ){

				$.sessionStorage.setItem('offset', temp );

			}else{

				$.sessionStorage.setItem('offset', 0 );
			}
			//e.preventDefault();
			//return false;
		};

		//attachRealOffset
		$('#eResults').on('click','.calendar-list-left-btm',attachRealOffset );
		$('#eResults').on('click','h3 a',attachRealOffset );
		$('#eResults').on('click','.calendar-list-left-body',attachRealOffset ) ;


	};//end of calendar pagination

	var intelligentPaginator = function(){

		//http://stackoverflow.com/questions/399867/custom-events-in-jquery
		//http://api.jquery.com/trigger/
		//http://api.jquery.com/bind/
		//http://css-tricks.com/custom-events-are-pretty-cool/

		//on document load look for the offset,
		//offset = getOffset
		//is it is more than 0 auto load ajax, starting from 1 to till it is equal to offset
		//off the custom event after it is loaded to prevent further autoload  of ajax

		$(document).ready(function(){


			$(document).trigger('kcStockholm.moreSearchResults');

		});

		$(document).on('kcStockholm.moreSearchResults',function(){

			var offset = $.sessionStorage.getItem('offset');
			if( offset > 0){

			}
			//call the autoload procedure
			$(document).off('kcStockholm.moreSearchResults');

		});
	}

	$(document).ready(function(){
		kc_buttons_fix();
		calendar_search_datepicker();
		calendar_search();
		calendar_pagination();

	})

})(jQuery)