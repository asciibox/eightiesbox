// index.js (entry point)
import Main from './static/bassoontracker/src/main.js';


import Host from '../static/bassoontracker/src/host.js';
import AmiBase from '../static/bassoontracker/hosts/AmiBase/amibase.js';
import HostBridge from '../static/bassoontracker/hosts/AmiBase/bridge.js';

import { cachedAssets, sprites, UI, PRELOADTYPE, EVENT, COMMAND, PLAYTYPE, FILETYPE, MODULETYPE, SAMPLETYPE, STEREOSEPARATION, FREQUENCYTABLE, LOOPTYPE, SELECTION, 
    EDITACTION, AMIGA_PALFREQUENCY, PC_FREQUENCY_HALF,LAYOUTS, NOTEPERIOD, FTNOTEPERIOD, NOTEOFF, KEYBOARDKEYS, OCTAVENOTES, KEYBOARDTABLE, TRACKERMODE, SETTINGS
     } from './static/bassoontracker/src/enum.js';

import EventBus from '../static/bassoontracker/src/eventBus.js';
import { loadFile, saveFile, BinaryStream} from './static/bassoontracker/src/filesystem.js';
import Audio from '../static/bassoontracker/src/audio.js';

import Note from '../static/bassoontracker/src/models/note.js';
import Instrument from '../static/bassoontracker/src/models/instrument.js';
import Sample from '../static/bassoontracker/src/models/sample.js';

 import { getUrlParameter, formatFileSize, createSlug}  from './static/bassoontracker/src/lib/util.js';


  import WAAClock from './static/bassoontracker/src/lib/waaclock.js';
  import saveAs from './static/bassoontracker/src/lib/filesaver.js';
  import { audioBufferToWav, encodeWAV } from './static/bassoontracker/src/lib/audioBufferToWav.js';
  import dropboxService from './static/bassoontracker/src/lib/dropbox.js';

import { getSamplerate } from './static/bassoontracker/src/audio/getSamplerate.js';
  import { readRAWsample } from './static/bassoontracker/src/audio/raw.js';
  import { read8SVXsample } from './static/bassoontracker/src/audio/8svx.js';
  import {encodeRIFFsample } from './static/bassoontracker/src/audio/riffWave.js';
  import {  detectSampleType,  decodeFileWithAudioContext } from './static/bassoontracker/src/audio/detectSampleType.js';
import FilterChain from '../static/bassoontracker/src/audio/filterChain.js';
import Midi from '../static/bassoontracker/src/audio/midi.js';

import Main from '../static/bassoontracker/src/main.js';
import App from '../static/bassoontracker/src/app.js';
import Tracker from '../static/bassoontracker/src/tracker.js';
import Editor from '../static/bassoontracker/src/editor.js';
import PreLoader from '../static/bassoontracker/src/preloader.js';
import FetchService from '../static/bassoontracker/src/fetchService.js';
import Storage from '../static/bassoontracker/src/storage.js';
import Settings from '../static/bassoontracker/src/settings.js';
import Logger from '../static/bassoontracker/src/log.js';

import Layout from '../static/bassoontracker/src/ui/app/layout.js';

import Y from '../static/bassoontracker/src/ui/yascal/yascal.js';

import UI from '../static/bassoontracker/src/ui/main.js';
import YascalSprite from '../static/bassoontracker/src/ui/yascal/sprite.js'; // Yascal.sprite

const Yascal = {
  sprite: YascalSprite
};




import UIAssets from '../static/bassoontracker/src/ui/assets.js';
import Input from '../static/bassoontracker/src/ui/input.js';
import UIticker from '../static/bassoontracker/src/ui/ticker.js';
import StateManager from '../static/bassoontracker/src/ui/stateManager.js';

import UIelement from '../static/bassoontracker/src/ui/components/element.js'; // UI.element
import UIpanel from '../static/bassoontracker/src/ui/components/panel.js'; // UI.panel
import UIimage from '../static/bassoontracker/src/ui/components/image.js'; // UI.image
import UIbutton from '../static/bassoontracker/src/ui/components/button.js'; // UI.button
import UIcheckboxbutton from '../static/bassoontracker/src/ui/components/checkboxbutton.js'; // UI.checkboxbutton
import UIlabel from '../static/bassoontracker/src/ui/components/label.js'; // UI.label
import UIinputbox from '../static/bassoontracker/src/ui/components/inputbox.js';
import UIlistbox from '../static/bassoontracker/src/ui/components/listbox.js';
import UIradioGroup from '../static/bassoontracker/src/ui/components/radiogroup.js';
import UIcheckbox from '../static/bassoontracker/src/ui/components/checkbox.js';
import UInumberDisplay from '../static/bassoontracker/src/ui/components/numberdisplay.js';
import UImodalDialog from '../static/bassoontracker/src/ui/components/modalDialog.js';
import UIscale9Panel from '../static/bassoontracker/src/ui/components/scale9.js';
  import {BitmapFont } from './static/bassoontracker/src/ui/components/bitmapfont.js';
import UIknob from '../static/bassoontracker/src/ui/components/knob.js';
import UIrangeSlider from '../static/bassoontracker/src/ui/components/rangeSlider.js';
import UImenu from '../static/bassoontracker/src/ui/components/menu.js';
import UIsubmenu from '../static/bassoontracker/src/ui/components/submenu.js';
import UIanimsprite from '../static/bassoontracker/src/ui/components/animsprite.js';


import UIapp_songPatternList from '../static/bassoontracker/src/ui/app/components/songPatternList.js';
import UIpattern_sidebar from '../static/bassoontracker/src/ui/app/components/patternSidebar.js';
import UIapp_sidebar from '../static/bassoontracker/src/ui/app/components/appSidebar.js';

import UIapp_panelContainer from '../static/bassoontracker/src/ui/app/panelContainer.js';
import UIapp_menu from '../static/bassoontracker/src/ui/app/menu.js';
  import UIapp_mainPanel from './static/bassoontracker/src/ui/app/mainPanel.js';
import UIapp_controlPanel from '../static/bassoontracker/src/ui/app/controlPanel.js';
import UIapp_patternPanel from '../static/bassoontracker/src/ui/app/patternPanel.js';

import UIMainPanel from '../static/bassoontracker/src/ui/mainPanel.js'; // STARTR
import UIapp_patternView from '../static/bassoontracker/src/ui/app/components/patternView.js';
import UIfxPanel from '../static/bassoontracker/src/ui/fxpanel.js';
import UISampleView from '../static/bassoontracker/src/ui/sampleView.js';
import UIDiskOperations from '../static/bassoontracker/src/ui/diskOperations.js';
import UIDiskOperationActions from '../static/bassoontracker/src/ui/diskOp_Actions.js';
import UIDiskOperationType from '../static/bassoontracker/src/ui/diskOp_Type.js';
import UIDiskOperationTargets from '../static/bassoontracker/src/ui/diskOp_Targets.js';
import UIDiskOperationSave from '../static/bassoontracker/src/ui/diskOp_Save.js';
import UIOptionsPanel from '../static/bassoontracker/src/ui/optionsPanel.js';
import UIapp_pianoView from '../static/bassoontracker/src/ui/app/pianoView.js';
import UIWaveForm from '../static/bassoontracker/src/ui/waveform.js';
import UIEnvelope from '../static/bassoontracker/src/ui/envelope.js';
import UIEnvelopePanel from '../static/bassoontracker/src/ui/envelopePanel.js';
import UIvisualiser from '../static/bassoontracker/src/ui/app/components/visualiser.js';
import UIvumeter from '../static/bassoontracker/src/ui/app/components/vumeter.js';
import UIspinBox from '../static/bassoontracker/src/ui/spinBox.js';
import UIsliderBox from '../static/bassoontracker/src/ui/sliderBox.js';
import UIeditPanel from '../static/bassoontracker/src/ui/editPanel.js';
import UIapp_songControl from '../static/bassoontracker/src/ui/app/components/songControl.js';
import UItrackControl from '../static/bassoontracker/src/ui/app/components/trackControl.js';
import UIbuttonGroup from '../static/bassoontracker/src/ui/app/components/buttonGroup.js';
import UIInfoPanel from '../static/bassoontracker/src/ui/infopanel.js'; // END

const UI = {
  Assets : UIAssets,
  ticker : UIticker,
  element : UIelement,
  panel : UIpanel,
  image : UIimage,
  button : UIbutton,
  checkboxbutton: UIcheckboxbutton,
  label : UIlabel,
  inputbox : UIinputbox,
  listbox : UIlistbox,
  radioGroup  :  UIradioGroup,
  checkbox : UIcheckbox,
  numberDisplay: UInumberDisplay,
  modalDialog : UImodalDialog,
  scale9Panel : UIscale9Panel,
  knob : UIknob,
  rangeSlider : UIrangeSlider,
  menu : UImenu,
  submenu : UIsubmenu,
  animsprite : UIanimsprite,
  app_songPatternList : UIapp_songPatternList,
  pattern_sidebar : UIpattern_sidebar,
  app_sidebar : UIapp_sidebar ,
  app_panelContainer : UIapp_panelContainer,
  menu : UIapp_menu,
  app_mainPanel: UIapp_mainPanel,
  app_controlPanel :  UIapp_controlPanel,
  app_patternPanel : UIapp_patternPanel,
  MainPanel : UIMainPanel,
  app_patternView: UIapp_patternView,
  fxPanel : UIfxPanel,
  SampleView : UISampleView,
  DiskOperations: UIDiskOperations,
  DiskOperationActions: UIDiskOperationActions,
  DiskOperationType: UIDiskOperationType,
  DiskOperationTargets: UIDiskOperationTargets,
  DiskOperationSave: UIDiskOperationSave,
  OptionsPanel: UIOptionsPanel,
  app_pianoView : UIapp_pianoView,
  WaveForm : UIWaveForm,
  Envelope : UIEnvelope,
  EnvelopePanel : UIEnvelopePanel,
  visualiser : UIvisualiser,
  vumeter: UIvumeter,
  spinBox: UIspinBox,
  sliderBox: UIsliderBox,
  editPanel : UIeditPanel,
  app_songControl : UIapp_songControl,
  trackControl : UItrackControl,
  buttonGroup : UIbuttonGroup,
  InfoPanel : UIInfoPanel,
};



import ModArchive from '../static/bassoontracker/src/provider/modarchive.js';
import ModulesPl from '../static/bassoontracker/src/provider/modulespl.js';
import Dropbox from '../static/bassoontracker/src/provider/dropbox.js';
import BassoonProvider from '../static/bassoontracker/src/provider/bassoon.js';

import FileDetector from '../static/bassoontracker/src/fileformats/detect.js';
import ProTracker from '../static/bassoontracker/src/fileformats/protracker.js';
import SoundTracker from '../static/bassoontracker/src/fileformats/soundtracker.js';
import FastTracker from '../static/bassoontracker/src/fileformats/fasttracker.js';

import zip from './static/bassoontracker/src/lib/zip.js';

import Plugin from './static/bassoontracker/plugins/loader.js';
