/**
 * Copyright (C) 2016 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Remote player data.
 * @type {!cast.framework.RemotePlayer}
 */
var player;


/**
 * The local player element
 * @type {Element}
 */
var localPlayer = document.getElementById('videoElement');


/**
 * Angular controller for the remote player.
 * @param {!angular.Scope} $scope the angular scope
 */
function playerController($scope) {
  // Remote player data.
  player = $scope.player = new cast.framework.RemotePlayer();

  // Remote player controller.
  $scope.controller = new cast.framework.RemotePlayerController(player);

  // Listen to any player update, and trigger angular data binding update.
  $scope.controller.addEventListener(
      cast.framework.RemotePlayerEventType.ANY_CHANGE,
      function(event) {
        if (!$scope.$$phase) $scope.$apply();
      });

  // Listen to cast connection/disconnection and continue playing video
  // locally or remotely. (Volume and mute states are not being transferred)
  $scope.controller.addEventListener(
      cast.framework.RemotePlayerEventType.IS_CONNECTED_CHANGED,
      function(event) {
        if (player.isConnected) {
          // Continue playing remotely what is playing locally.
          if (localPlayer.src) {
            // If local playback is done, do not play on remote
            if (localPlayer.currentTime < localPlayer.duration) {
              playRemote(
                  getMediaIndex(localPlayer.src),
                  localPlayer.currentTime,
                  localPlayer.paused);
              localPlayer.removeAttribute('src');
              localPlayer.load();
            }
          }
        } else {
          // Continue playing locally what is playing locally.
          if (player.savedPlayerState &&
              player.savedPlayerState.mediaInfo) {
            var mediaId = getMediaIndex(
                player.savedPlayerState.mediaInfo.contentId);
            if (mediaId >= 0) {
              playLocally(
                  mediaId,
                  player.savedPlayerState.currentTime,
                  player.savedPlayerState.isPaused);
            } else {
              console.log('Unknown media is playing ' +
                  player.savedPlayerState.mediaInfo.contentId);
            }
          }
        }
      });

  // Handle seek click event.
  $scope.seekClick = function($event) {
    if (player.canSeek) {
      var percent = 100 * $event.offsetX / $event.currentTarget.offsetWidth;
      player.currentTime =
          player.controller.getSeekTime(percent, player.duration);
      player.controller.seek();
    }
  };

  // Handle volume click event.
  $scope.volumeClick = function($event) {
    if (player.isConnected) {
      player.volumeLevel = $event.offsetX / $event.currentTarget.offsetWidth;
      player.controller.setVolumeLevel();
    }
  };

  // Get seek position (percentage) according to player current time.
  $scope.getSeekPosition = function() {
    return player.controller.getSeekPosition(
        player.currentTime, player.duration);
  };

  // Get a display string to show current seek time.
  $scope.getSeekString = function() {
    return player.controller.getFormattedTime(player.currentTime) + ' / ' +
        player.controller.getFormattedTime(player.duration);
  };
}


/**
 * Initialize cast service.
 * @param {boolean} isAvailable
 * @param {?string} reason
 */
window['__onGCastApiAvailable'] = function(isAvailable, reason) {

  if (isAvailable) {
    // Init cast
    cast.framework.CastContext.getInstance().setOptions({
      receiverApplicationId: chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID,
      autoJoinPolicy: chrome.cast.AutoJoinPolicy.ORIGIN_SCOPED
    });
  } else {
    document.getElementById('castDiv').style.display = 'none';
    document.getElementById('playerControl').style.display = 'none';
    document.getElementById('castError').innerText = reason;
  }

  // Initialize angular
  var app = angular.module('CastVideo', []);
  app.controller('PlayerController', playerController);
  angular.bootstrap(document, ['CastVideo']);
};


var MEDIA_SOURCE_ROOT =
    'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/';


/**
 * Available media.
 */
var MEDIA_CONTENT = [
  {
    'source': MEDIA_SOURCE_ROOT + 'BigBuckBunny.mp4',
    'title': 'Big Buck Bunny',
    'subtitle': 'By Blender Foundation',
    'thumb': MEDIA_SOURCE_ROOT + 'images/BigBuckBunny.jpg',
    'contentType': 'video/mp4',
    'description': 'Big Buck Bunny tells the story of a giant rabbit with a heart bigger than himself. When one sunny day three rodents rudely harass him, something snaps... and the rabbit ain\'t no bunny anymore! In the typical cartoon tradition he prepares the nasty rodents a comical revenge.\n\nLicensed under the Creative Commons Attribution license\nhttp://www.bigbuckbunny.org'
  },
  {
    'source': MEDIA_SOURCE_ROOT + 'Sintel.mp4',
    'title': 'Sintel',
    'subtitle': 'By Blender Foundation',
    'thumb': MEDIA_SOURCE_ROOT + 'images/Sintel.jpg',
    'contentType': 'video/mp4',
    'description' : 'Sintel is an independently produced short film, initiated by the Blender Foundation as a means to further improve and validate the free/open source 3D creation suite Blender. With initial funding provided by 1000s of donations via the internet community, it has again proven to be a viable development model for both open 3D technology as for independent animation film.\nThis 15 minute film has been realized in the studio of the Amsterdam Blender Institute, by an international team of artists and developers. In addition to that, several crucial technical and creative targets have been realized online, by developers and artists and teams all over the world.\nwww.sintel.org'
  }
];

function getMediaIndex(source) {
  for (var i = 0 ; i < MEDIA_CONTENT.length; i++) {
    if (MEDIA_CONTENT[i]['source'] == source) {
      return i;
    }
  }
  return -1;
}

/**
 * Start playing media on remote device.
 * @param {number} mediaIndex Media index.
 */
function playMedia(mediaIndex) {
  if (player.isConnected) {
    playRemote(mediaIndex, 0, false);
  } else {
    playLocally(mediaIndex, 0, false);
  }
}


/**
 * Play media on remote device.
 * @param {number} mediaIndex Media index.
 * @param {number} currentTime Seek time into the media.
 * @param {boolean} isPaused Media will start paused if true;
 */
function playRemote(mediaIndex, currentTime, isPaused) {
  var session = cast.framework.CastContext.getInstance().getCurrentSession();
  if (session) {
    var content = MEDIA_CONTENT[mediaIndex];
    var mediaInfo = new chrome.cast.media.MediaInfo(
        content['source'], content['contentType']);
    mediaInfo.metadata = new chrome.cast.media.GenericMediaMetadata();
    mediaInfo.metadata.title = content['title'];
    mediaInfo.metadata.subtitle = content['subtitle'];
    mediaInfo.metadata.images = [{'url': content['thumb']}];
    var request = new chrome.cast.media.LoadRequest(mediaInfo);
    request.currentTime = currentTime;
    request.autoplay = !isPaused;
    session.loadMedia(request).then(
        function() { console.log('Load succeed'); },
        function(e) { console.log('Load failed ' + e); });
  }
}


/**
 * Play media on local player.
 * @param {number} mediaIndex Media index.
 * @param {number} currentTime Seek time into the media.
 * @param {boolean} isPaused Media will start paused if true;
 */
function playLocally(mediaIndex, currentTime, isPaused) {
  var content = MEDIA_CONTENT[mediaIndex];
  localPlayer.src = content['source'];
  localPlayer.currentTime = currentTime;
  localPlayer.load();
  if (isPaused) {
    localPlayer.pause();
  } else {
    localPlayer.play();
  }
}
