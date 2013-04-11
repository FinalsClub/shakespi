if (Meteor.isClient) {
  //
  Meteor.subscribe('romeo');
  Template.hello.greeting = function () {
    return "Welcome to shakespi.";
  };

  Template.hello.linesByRomeo = function () {
    //var lines = new Array;
    return Lines.find({speaker_text:'ROMEO'}).fetch();
  };

  Template.hello.events({
    'click input' : function () {
      // template data, if any, is available in 'this'
      if (typeof console !== 'undefined')

        console.log("You pressed the button");
    }
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // publish All Lines in Romeo and Juliet to the client
    Meteor.publish("romeo", function() {
      return Lines.find({play_title:"ROMEO AND JULIET"});
    });
  });
}
