var fns = [
  'alls_well_that_ends_well_moby.json',
  'antony_and_cleopatra_moby.json',
  'as_you_like_it_moby.json',
  'comedy_of_errors_moby.json',
  'coriolanus_moby.json',
  'cymbeline_moby.json',
  'hamlet_moby.json',
  'henry_iv_part_i_moby.json',
  'henry_iv_part_ii_moby.json',
  'henry_v_moby.json',
  'henry_vi_part_1_moby.json',
  'henry_vi_part_2_moby.json',
  'henry_vi_part_3_moby.json',
  'henry_viii_moby.json',
  'julius_caesar_moby.json',
  'lear_moby.json',
  'life_and_death_of_king_john_moby.json',
  'loves_labors_lost_moby.json',
  'macbeth_moby.json',
  'measure_for_measure_moby.json',
  'merchant_of_venice_moby.json',
  'merry_wives_of_windsor_moby.json',
  'midsummer_nights_dream_moby.json',
  'much_ado_about_nothing_moby.json',
  'othello_moby.json',
  'pericles_moby.json',
  'richard_ii_moby.json',
  'richard_iii_moby.json',
  'romeo_and_juliet_moby.json',
  'taming_of_the_shrew_moby.json',
  'tempest_moby.json',
  'timon_of_athens_moby.json',
  'titus_andronicus_moby.json',
  'troilus_and_cressida_moby.json',
  'twelfth_night_moby.json',
  'two_gentlemen_of_verona_moby.json',
  'winters_tale_moby.json'
]

Meteor.startup(function() {
  console.log('Server is starting');
  console.log('Total Plays:', Plays.find({}).count());

  if (Plays.find({}).count() === 0) {
    for (var i = 0; i < fns.length; i++) {

      var filename = fns[i];

      Meteor.http.get("http://localhost:3000/" + filename, function(error, response) {

        if (error) { return console.log(error); }

        var object = response.data;
        Plays.insert(object);
        console.log('Inserted:', object.title);
      }); // Meteor.get
    } // iterate over file names 
  } // if 

  console.log('Server Started');
});

