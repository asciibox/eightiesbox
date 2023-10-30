var SimpleKeyboard;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it declares 'SimpleKeyboard' on top-level, which conflicts with the current library output.
(() => {
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  SimpleKeyboard: () => (/* reexport */ Keyboard),
  "default": () => (/* binding */ index_modern)
});

;// CONCATENATED MODULE: ./src/lib/services/KeyboardLayout.ts
var getDefaultLayout = function getDefaultLayout() {
  return {
    "default": ["` 1 2 3 4 5 6 7 8 9 0 - = {bksp}", "{tab} q w e r t y u i o p [ ] \\", "{lock} a s d f g h j k l ; ' {enter}", "{shift} z x c v b n m , . / {shift}", ".com @ {space}"],
    shift: ["~ ! @ # $ % ^ & * ( ) _ + {bksp}", "{tab} Q W E R T Y U I O P { } |", '{lock} A S D F G H J K L : " {enter}', "{shift} Z X C V B N M < > ? {shift}", ".com @ {space}"]
  };
};
;// CONCATENATED MODULE: ./src/lib/services/Utilities.ts
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }
function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }
function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }
function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }
function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }
function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, _toPropertyKey(descriptor.key), descriptor); } }
function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function _defineProperty(obj, key, value) { key = _toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }
/**
 * Utility Service
 */
var Utilities = /*#__PURE__*/function () {
  /**
   * Creates an instance of the Utility service
   */
  function Utilities(_ref) {
    var getOptions = _ref.getOptions,
      getCaretPosition = _ref.getCaretPosition,
      getCaretPositionEnd = _ref.getCaretPositionEnd,
      dispatch = _ref.dispatch;
    _classCallCheck(this, Utilities);
    _defineProperty(this, "getOptions", void 0);
    _defineProperty(this, "getCaretPosition", void 0);
    _defineProperty(this, "getCaretPositionEnd", void 0);
    _defineProperty(this, "dispatch", void 0);
    _defineProperty(this, "maxLengthReached", void 0);
    /**
     * Check whether the button is a standard button
     */
    _defineProperty(this, "isStandardButton", function (button) {
      return button && !(button[0] === "{" && button[button.length - 1] === "}");
    });
    this.getOptions = getOptions;
    this.getCaretPosition = getCaretPosition;
    this.getCaretPositionEnd = getCaretPositionEnd;
    this.dispatch = dispatch;

    /**
     * Bindings
     */
    Utilities.bindMethods(Utilities, this);
  }

  /**
   * Retrieve button type
   *
   * @param  {string} button The button's layout name
   * @return {string} The button type
   */
  _createClass(Utilities, [{
    key: "getButtonType",
    value: function getButtonType(button) {
      return button.includes("{") && button.includes("}") && button !== "{//}" ? "functionBtn" : "standardBtn";
    }

    /**
     * Adds default classes to a given button
     *
     * @param  {string} button The button's layout name
     * @return {string} The classes to be added to the button
     */
  }, {
    key: "getButtonClass",
    value: function getButtonClass(button) {
      var buttonTypeClass = this.getButtonType(button);
      var buttonWithoutBraces = button.replace("{", "").replace("}", "");
      var buttonNormalized = "";
      if (buttonTypeClass !== "standardBtn") buttonNormalized = " hg-button-".concat(buttonWithoutBraces);
      return "hg-".concat(buttonTypeClass).concat(buttonNormalized);
    }

    /**
     * Default button display labels
     */
  }, {
    key: "getDefaultDiplay",
    value: function getDefaultDiplay() {
      return {
        "{bksp}": "backspace",
        "{backspace}": "backspace",
        "{enter}": "< enter",
        "{shift}": "shift",
        "{shiftleft}": "shift",
        "{shiftright}": "shift",
        "{alt}": "alt",
        "{s}": "shift",
        "{tab}": "tab",
        "{lock}": "caps",
        "{capslock}": "caps",
        "{accept}": "Submit",
        "{space}": " ",
        "{//}": " ",
        "{esc}": "esc",
        "{escape}": "esc",
        "{f1}": "f1",
        "{f2}": "f2",
        "{f3}": "f3",
        "{f4}": "f4",
        "{f5}": "f5",
        "{f6}": "f6",
        "{f7}": "f7",
        "{f8}": "f8",
        "{f9}": "f9",
        "{f10}": "f10",
        "{f11}": "f11",
        "{f12}": "f12",
        "{numpaddivide}": "/",
        "{numlock}": "lock",
        "{arrowup}": "↑",
        "{arrowleft}": "←",
        "{arrowdown}": "↓",
        "{arrowright}": "→",
        "{prtscr}": "print",
        "{scrolllock}": "scroll",
        "{pause}": "pause",
        "{insert}": "ins",
        "{home}": "home",
        "{pageup}": "up",
        "{delete}": "del",
        "{forwarddelete}": "del",
        "{end}": "end",
        "{pagedown}": "down",
        "{numpadmultiply}": "*",
        "{numpadsubtract}": "-",
        "{numpadadd}": "+",
        "{numpadenter}": "enter",
        "{period}": ".",
        "{numpaddecimal}": ".",
        "{numpad0}": "0",
        "{numpad1}": "1",
        "{numpad2}": "2",
        "{numpad3}": "3",
        "{numpad4}": "4",
        "{numpad5}": "5",
        "{numpad6}": "6",
        "{numpad7}": "7",
        "{numpad8}": "8",
        "{numpad9}": "9"
      };
    }
    /**
     * Returns the display (label) name for a given button
     *
     * @param  {string} button The button's layout name
     * @param  {object} display The provided display option
     * @param  {boolean} mergeDisplay Whether the provided param value should be merged with the default one.
     */
  }, {
    key: "getButtonDisplayName",
    value: function getButtonDisplayName(button, display) {
      var mergeDisplay = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
      if (mergeDisplay) {
        display = Object.assign({}, this.getDefaultDiplay(), display);
      } else {
        display = display || this.getDefaultDiplay();
      }
      return display[button] || button;
    }

    /**
     * Returns the updated input resulting from clicking a given button
     *
     * @param  {string} button The button's layout name
     * @param  {string} input The input string
     * @param  {number} caretPos The cursor's current position
     * @param  {number} caretPosEnd The cursor's current end position
     * @param  {boolean} moveCaret Whether to update simple-keyboard's cursor
     */
  }, {
    key: "getUpdatedInput",
    value: function getUpdatedInput(button, input, caretPos) {
      var caretPosEnd = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : caretPos;
      var moveCaret = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : false;
      var options = this.getOptions();
      var commonParams = [caretPos, caretPosEnd, moveCaret];
      var output = input;
      if ((button === "{bksp}" || button === "{backspace}") && output.length > 0) {
        output = this.removeAt.apply(this, [output].concat(commonParams));
      } else if ((button === "{delete}" || button === "{forwarddelete}") && output.length > 0) {
        output = this.removeForwardsAt.apply(this, [output].concat(commonParams));
      } else if (button === "{space}") output = this.addStringAt.apply(this, [output, " "].concat(commonParams));else if (button === "{tab}" && !(typeof options.tabCharOnTab === "boolean" && options.tabCharOnTab === false)) {
        output = this.addStringAt.apply(this, [output, "\t"].concat(commonParams));
      } else if ((button === "{enter}" || button === "{numpadenter}") && options.newLineOnEnter) output = this.addStringAt.apply(this, [output, "\n"].concat(commonParams));else if (button.includes("numpad") && Number.isInteger(Number(button[button.length - 2]))) {
        output = this.addStringAt.apply(this, [output, button[button.length - 2]].concat(commonParams));
      } else if (button === "{numpaddivide}") output = this.addStringAt.apply(this, [output, "/"].concat(commonParams));else if (button === "{numpadmultiply}") output = this.addStringAt.apply(this, [output, "*"].concat(commonParams));else if (button === "{numpadsubtract}") output = this.addStringAt.apply(this, [output, "-"].concat(commonParams));else if (button === "{numpadadd}") output = this.addStringAt.apply(this, [output, "+"].concat(commonParams));else if (button === "{numpaddecimal}") output = this.addStringAt.apply(this, [output, "."].concat(commonParams));else if (button === "{" || button === "}") output = this.addStringAt.apply(this, [output, button].concat(commonParams));else if (!button.includes("{") && !button.includes("}")) output = this.addStringAt.apply(this, [output, button].concat(commonParams));
      if (options.debug) {
        console.log("Input will be: " + output);
      }
      return output;
    }

    /**
     * Moves the cursor position by a given amount
     *
     * @param  {number} length Represents by how many characters the input should be moved
     * @param  {boolean} minus Whether the cursor should be moved to the left or not.
     */
  }, {
    key: "updateCaretPos",
    value: function updateCaretPos(length) {
      var minus = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;
      var newCaretPos = this.updateCaretPosAction(length, minus);
      this.dispatch(function (instance) {
        instance.setCaretPosition(newCaretPos);
      });
    }

    /**
     * Action method of updateCaretPos
     *
     * @param  {number} length Represents by how many characters the input should be moved
     * @param  {boolean} minus Whether the cursor should be moved to the left or not.
     */
  }, {
    key: "updateCaretPosAction",
    value: function updateCaretPosAction(length) {
      var minus = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;
      var options = this.getOptions();
      var caretPosition = this.getCaretPosition();
      if (caretPosition != null) {
        if (minus) {
          if (caretPosition > 0) caretPosition = caretPosition - length;
        } else {
          caretPosition = caretPosition + length;
        }
      }
      if (options.debug) {
        console.log("Caret at:", caretPosition);
      }
      return caretPosition;
    }

    /**
     * Adds a string to the input at a given position
     *
     * @param  {string} source The source input
     * @param  {string} str The string to add
     * @param  {number} position The (cursor) position where the string should be added
     * @param  {boolean} moveCaret Whether to update simple-keyboard's cursor
     */
  }, {
    key: "addStringAt",
    value: function addStringAt(source, str) {
      var position = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : source.length;
      var positionEnd = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : source.length;
      var moveCaret = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : false;
      var output;
      if (!position && position !== 0) {
        output = source + str;
      } else {
        output = [source.slice(0, position), str, source.slice(positionEnd)].join("");

        /**
         * Avoid caret position change when maxLength is set
         */
        if (!this.isMaxLengthReached()) {
          if (moveCaret) this.updateCaretPos(str.length);
        }
      }
      return output;
    }
  }, {
    key: "removeAt",
    value:
    /**
     * Removes an amount of characters before a given position
     *
     * @param  {string} source The source input
     * @param  {number} position The (cursor) position from where the characters should be removed
     * @param  {boolean} moveCaret Whether to update simple-keyboard's cursor
     */
    function removeAt(source) {
      var position = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : source.length;
      var positionEnd = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : source.length;
      var moveCaret = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : false;
      if (position === 0 && positionEnd === 0) {
        return source;
      }
      var output;
      if (position === positionEnd) {
        var prevTwoChars;
        var emojiMatched;
        var emojiMatchedReg = /([\uD800-\uDBFF][\uDC00-\uDFFF])/g;

        /**
         * Emojis are made out of two characters, so we must take a custom approach to trim them.
         * For more info: https://mathiasbynens.be/notes/javascript-unicode
         */
        if (position && position >= 0) {
          prevTwoChars = source.substring(position - 2, position);
          emojiMatched = prevTwoChars.match(emojiMatchedReg);
          if (emojiMatched) {
            output = source.substr(0, position - 2) + source.substr(position);
            if (moveCaret) this.updateCaretPos(2, true);
          } else {
            output = source.substr(0, position - 1) + source.substr(position);
            if (moveCaret) this.updateCaretPos(1, true);
          }
        } else {
          prevTwoChars = source.slice(-2);
          emojiMatched = prevTwoChars.match(emojiMatchedReg);
          if (emojiMatched) {
            output = source.slice(0, -2);
            if (moveCaret) this.updateCaretPos(2, true);
          } else {
            output = source.slice(0, -1);
            if (moveCaret) this.updateCaretPos(1, true);
          }
        }
      } else {
        output = source.slice(0, position) + source.slice(positionEnd);
        if (moveCaret) {
          this.dispatch(function (instance) {
            instance.setCaretPosition(position);
          });
        }
      }
      return output;
    }

    /**
     * Removes an amount of characters after a given position
     *
     * @param  {string} source The source input
     * @param  {number} position The (cursor) position from where the characters should be removed
     */
  }, {
    key: "removeForwardsAt",
    value: function removeForwardsAt(source) {
      var position = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : source.length;
      var positionEnd = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : source.length;
      var moveCaret = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : false;
      if (!(source !== null && source !== void 0 && source.length) || position === null) {
        return source;
      }
      var output;
      if (position === positionEnd) {
        var emojiMatchedReg = /([\uD800-\uDBFF][\uDC00-\uDFFF])/g;

        /**
         * Emojis are made out of two characters, so we must take a custom approach to trim them.
         * For more info: https://mathiasbynens.be/notes/javascript-unicode
         */
        var nextTwoChars = source.substring(position, position + 2);
        var emojiMatched = nextTwoChars.match(emojiMatchedReg);
        if (emojiMatched) {
          output = source.substr(0, position) + source.substr(position + 2);
        } else {
          output = source.substr(0, position) + source.substr(position + 1);
        }
      } else {
        output = source.slice(0, position) + source.slice(positionEnd);
        if (moveCaret) {
          this.dispatch(function (instance) {
            instance.setCaretPosition(position);
          });
        }
      }
      return output;
    }

    /**
     * Determines whether the maxLength has been reached. This function is called when the maxLength option it set.
     *
     * @param  {object} inputObj
     * @param  {string} updatedInput
     */
  }, {
    key: "handleMaxLength",
    value: function handleMaxLength(inputObj, updatedInput) {
      var options = this.getOptions();
      var maxLength = options.maxLength;
      var currentInput = inputObj[options.inputName || "default"];
      var condition = updatedInput.length - 1 >= maxLength;
      if (
      /**
       * If pressing this button won't add more characters
       * We exit out of this limiter function
       */
      updatedInput.length <= currentInput.length) {
        return false;
      }
      if (Number.isInteger(maxLength)) {
        if (options.debug) {
          console.log("maxLength (num) reached:", condition);
        }
        if (condition) {
          /**
           * @type {boolean} Boolean value that shows whether maxLength has been reached
           */
          this.maxLengthReached = true;
          return true;
        } else {
          this.maxLengthReached = false;
          return false;
        }
      }
      if (_typeof(maxLength) === "object") {
        var _condition = updatedInput.length - 1 >= maxLength[options.inputName || "default"];
        if (options.debug) {
          console.log("maxLength (obj) reached:", _condition);
        }
        if (_condition) {
          this.maxLengthReached = true;
          return true;
        } else {
          this.maxLengthReached = false;
          return false;
        }
      }
    }

    /**
     * Gets the current value of maxLengthReached
     */
  }, {
    key: "isMaxLengthReached",
    value: function isMaxLengthReached() {
      return Boolean(this.maxLengthReached);
    }

    /**
     * Determines whether a touch device is being used
     */
  }, {
    key: "isTouchDevice",
    value: function isTouchDevice() {
      return "ontouchstart" in window || navigator.maxTouchPoints;
    }

    /**
     * Determines whether pointer events are supported
     */
  }, {
    key: "pointerEventsSupported",
    value: function pointerEventsSupported() {
      return !!window.PointerEvent;
    }

    /**
     * Bind all methods in a given class
     */
  }, {
    key: "camelCase",
    value:
    /**
     * Transforms an arbitrary string to camelCase
     *
     * @param  {string} str The string to transform.
     */
    function camelCase(str) {
      if (!str) return "";
      return str.toLowerCase().trim().split(/[.\-_\s]/g).reduce(function (str, word) {
        return word.length ? str + word[0].toUpperCase() + word.slice(1) : str;
      });
    }

    /**
     * Split array into chunks
     */
  }, {
    key: "chunkArray",
    value: function chunkArray(arr, size) {
      return _toConsumableArray(Array(Math.ceil(arr.length / size))).map(function (_, i) {
        return arr.slice(size * i, size + size * i);
      });
    }

    /**
     * Escape regex input
     */
  }, {
    key: "escapeRegex",
    value: function escapeRegex(str) {
      return str.replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&");
    }

    /**
     * Calculate caret position offset when using rtl option
     */
  }, {
    key: "getRtlOffset",
    value: function getRtlOffset(index, input) {
      var newIndex = index;
      var startMarkerIndex = input.indexOf("\u202B");
      var endMarkerIndex = input.indexOf("\u202C");
      if (startMarkerIndex < index && startMarkerIndex != -1) {
        newIndex--;
      }
      if (endMarkerIndex < index && startMarkerIndex != -1) {
        newIndex--;
      }
      return newIndex < 0 ? 0 : newIndex;
    }

    /**
     * Reusable empty function
     */
  }], [{
    key: "bindMethods",
    value: function bindMethods(myClass, instance) {
      // eslint-disable-next-line no-unused-vars
      var _iterator = _createForOfIteratorHelper(Object.getOwnPropertyNames(myClass.prototype)),
        _step;
      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var myMethod = _step.value;
          var excludeMethod = myMethod === "constructor" || myMethod === "bindMethods";
          if (!excludeMethod) {
            instance[myMethod] = instance[myMethod].bind(instance);
          }
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
    }
  }]);
  return Utilities;
}();
_defineProperty(Utilities, "noop", function () {});
/* harmony default export */ const services_Utilities = (Utilities);
;// CONCATENATED MODULE: ./src/lib/services/PhysicalKeyboard.ts
function PhysicalKeyboard_typeof(o) { "@babel/helpers - typeof"; return PhysicalKeyboard_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, PhysicalKeyboard_typeof(o); }
function PhysicalKeyboard_classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function PhysicalKeyboard_defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, PhysicalKeyboard_toPropertyKey(descriptor.key), descriptor); } }
function PhysicalKeyboard_createClass(Constructor, protoProps, staticProps) { if (protoProps) PhysicalKeyboard_defineProperties(Constructor.prototype, protoProps); if (staticProps) PhysicalKeyboard_defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function PhysicalKeyboard_defineProperty(obj, key, value) { key = PhysicalKeyboard_toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function PhysicalKeyboard_toPropertyKey(arg) { var key = PhysicalKeyboard_toPrimitive(arg, "string"); return PhysicalKeyboard_typeof(key) === "symbol" ? key : String(key); }
function PhysicalKeyboard_toPrimitive(input, hint) { if (PhysicalKeyboard_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (PhysicalKeyboard_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }


/**
 * Physical Keyboard Service
 */
var PhysicalKeyboard = /*#__PURE__*/function () {
  /**
   * Creates an instance of the PhysicalKeyboard service
   */
  function PhysicalKeyboard(_ref) {
    var _this = this;
    var dispatch = _ref.dispatch,
      getOptions = _ref.getOptions;
    PhysicalKeyboard_classCallCheck(this, PhysicalKeyboard);
    PhysicalKeyboard_defineProperty(this, "getOptions", void 0);
    PhysicalKeyboard_defineProperty(this, "dispatch", void 0);
    PhysicalKeyboard_defineProperty(this, "isMofifierKey", function (e) {
      return e.altKey || e.ctrlKey || e.shiftKey || ["Tab", "CapsLock", "Esc", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code || e.key || _this.keyCodeToKey(e === null || e === void 0 ? void 0 : e.keyCode));
    });
    /**
     * @type {object} A simple-keyboard instance
     */
    this.dispatch = dispatch;
    this.getOptions = getOptions;

    /**
     * Bindings
     */
    services_Utilities.bindMethods(PhysicalKeyboard, this);
  }
  PhysicalKeyboard_createClass(PhysicalKeyboard, [{
    key: "handleHighlightKeyDown",
    value: function handleHighlightKeyDown(e) {
      var options = this.getOptions();
      if (options.physicalKeyboardHighlightPreventDefault && this.isMofifierKey(e)) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
      var buttonPressed = this.getSimpleKeyboardLayoutKey(e);
      this.dispatch(function (instance) {
        var standardButtonPressed = instance.getButtonElement(buttonPressed);
        var functionButtonPressed = instance.getButtonElement("{".concat(buttonPressed, "}"));
        var buttonDOM;
        var buttonName;
        if (standardButtonPressed) {
          buttonDOM = standardButtonPressed;
          buttonName = buttonPressed;
        } else if (functionButtonPressed) {
          buttonDOM = functionButtonPressed;
          buttonName = "{".concat(buttonPressed, "}");
        } else {
          return;
        }
        var applyButtonStyle = function applyButtonStyle(buttonElement) {
          buttonElement.style.background = options.physicalKeyboardHighlightBgColor || "#dadce4";
          buttonElement.style.color = options.physicalKeyboardHighlightTextColor || "black";
        };
        if (buttonDOM) {
          if (Array.isArray(buttonDOM)) {
            buttonDOM.forEach(function (buttonElement) {
              return applyButtonStyle(buttonElement);
            });

            // Even though we have an array of buttons, we just want to press one of them
            if (options.physicalKeyboardHighlightPress) {
              if (options.physicalKeyboardHighlightPressUsePointerEvents) {
                var _buttonDOM$;
                (_buttonDOM$ = buttonDOM[0]) === null || _buttonDOM$ === void 0 || _buttonDOM$.onpointerdown();
              } else if (options.physicalKeyboardHighlightPressUseClick) {
                var _buttonDOM$2;
                (_buttonDOM$2 = buttonDOM[0]) === null || _buttonDOM$2 === void 0 || _buttonDOM$2.click();
              } else {
                instance.handleButtonClicked(buttonName, e);
              }
            }
          } else {
            applyButtonStyle(buttonDOM);
            if (options.physicalKeyboardHighlightPress) {
              if (options.physicalKeyboardHighlightPressUsePointerEvents) {
                buttonDOM.onpointerdown();
              } else if (options.physicalKeyboardHighlightPressUseClick) {
                buttonDOM.click();
              } else {
                instance.handleButtonClicked(buttonName, e);
              }
            }
          }
        }
      });
    }
  }, {
    key: "handleHighlightKeyUp",
    value: function handleHighlightKeyUp(e) {
      var options = this.getOptions();
      if (options.physicalKeyboardHighlightPreventDefault && this.isMofifierKey(e)) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
      var buttonPressed = this.getSimpleKeyboardLayoutKey(e);
      this.dispatch(function (instance) {
        var buttonDOM = instance.getButtonElement(buttonPressed) || instance.getButtonElement("{".concat(buttonPressed, "}"));
        var applyButtonStyle = function applyButtonStyle(buttonElement) {
          if (buttonElement.removeAttribute) {
            buttonElement.removeAttribute("style");
          }
        };
        if (buttonDOM) {
          if (Array.isArray(buttonDOM)) {
            buttonDOM.forEach(function (buttonElement) {
              return applyButtonStyle(buttonElement);
            });

            // Even though we have an array of buttons, we just want to press one of them
            if (options.physicalKeyboardHighlightPressUsePointerEvents) {
              var _buttonDOM$3;
              (_buttonDOM$3 = buttonDOM[0]) === null || _buttonDOM$3 === void 0 || _buttonDOM$3.onpointerup();
            }
          } else {
            applyButtonStyle(buttonDOM);
            if (options.physicalKeyboardHighlightPressUsePointerEvents) {
              buttonDOM.onpointerup();
            }
          }
        }
      });
    }

    /**
     * Transforms a KeyboardEvent's "key.code" string into a simple-keyboard layout format
     * @param  {object} e The KeyboardEvent
     */
  }, {
    key: "getSimpleKeyboardLayoutKey",
    value: function getSimpleKeyboardLayoutKey(e) {
      var _output;
      var output = "";
      var keyId = e.code || e.key || this.keyCodeToKey(e === null || e === void 0 ? void 0 : e.keyCode);
      if (keyId !== null && keyId !== void 0 && keyId.includes("Numpad") || keyId !== null && keyId !== void 0 && keyId.includes("Shift") || keyId !== null && keyId !== void 0 && keyId.includes("Space") || keyId !== null && keyId !== void 0 && keyId.includes("Backspace") || keyId !== null && keyId !== void 0 && keyId.includes("Control") || keyId !== null && keyId !== void 0 && keyId.includes("Alt") || keyId !== null && keyId !== void 0 && keyId.includes("Meta")) {
        output = e.code || "";
      } else {
        output = e.key || this.keyCodeToKey(e === null || e === void 0 ? void 0 : e.keyCode) || "";
      }
      return output.length > 1 ? (_output = output) === null || _output === void 0 ? void 0 : _output.toLowerCase() : output;
    }

    /**
     * Retrieve key from keyCode
     */
  }, {
    key: "keyCodeToKey",
    value: function keyCodeToKey(keyCode) {
      return {
        8: "Backspace",
        9: "Tab",
        13: "Enter",
        16: "Shift",
        17: "Ctrl",
        18: "Alt",
        19: "Pause",
        20: "CapsLock",
        27: "Esc",
        32: "Space",
        33: "PageUp",
        34: "PageDown",
        35: "End",
        36: "Home",
        37: "ArrowLeft",
        38: "ArrowUp",
        39: "ArrowRight",
        40: "ArrowDown",
        45: "Insert",
        46: "Delete",
        48: "0",
        49: "1",
        50: "2",
        51: "3",
        52: "4",
        53: "5",
        54: "6",
        55: "7",
        56: "8",
        57: "9",
        65: "A",
        66: "B",
        67: "C",
        68: "D",
        69: "E",
        70: "F",
        71: "G",
        72: "H",
        73: "I",
        74: "J",
        75: "K",
        76: "L",
        77: "M",
        78: "N",
        79: "O",
        80: "P",
        81: "Q",
        82: "R",
        83: "S",
        84: "T",
        85: "U",
        86: "V",
        87: "W",
        88: "X",
        89: "Y",
        90: "Z",
        91: "Meta",
        96: "Numpad0",
        97: "Numpad1",
        98: "Numpad2",
        99: "Numpad3",
        100: "Numpad4",
        101: "Numpad5",
        102: "Numpad6",
        103: "Numpad7",
        104: "Numpad8",
        105: "Numpad9",
        106: "NumpadMultiply",
        107: "NumpadAdd",
        109: "NumpadSubtract",
        110: "NumpadDecimal",
        111: "NumpadDivide",
        112: "F1",
        113: "F2",
        114: "F3",
        115: "F4",
        116: "F5",
        117: "F6",
        118: "F7",
        119: "F8",
        120: "F9",
        121: "F10",
        122: "F11",
        123: "F12",
        144: "NumLock",
        145: "ScrollLock",
        186: ";",
        187: "=",
        188: ",",
        189: "-",
        190: ".",
        191: "/",
        192: "`",
        219: "[",
        220: "\\",
        221: "]",
        222: "'"
      }[keyCode] || "";
    }
  }]);
  return PhysicalKeyboard;
}();
/* harmony default export */ const services_PhysicalKeyboard = (PhysicalKeyboard);
;// CONCATENATED MODULE: ./src/lib/components/CandidateBox.ts
function CandidateBox_typeof(o) { "@babel/helpers - typeof"; return CandidateBox_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, CandidateBox_typeof(o); }
function CandidateBox_classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function CandidateBox_defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, CandidateBox_toPropertyKey(descriptor.key), descriptor); } }
function CandidateBox_createClass(Constructor, protoProps, staticProps) { if (protoProps) CandidateBox_defineProperties(Constructor.prototype, protoProps); if (staticProps) CandidateBox_defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function CandidateBox_defineProperty(obj, key, value) { key = CandidateBox_toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function CandidateBox_toPropertyKey(arg) { var key = CandidateBox_toPrimitive(arg, "string"); return CandidateBox_typeof(key) === "symbol" ? key : String(key); }
function CandidateBox_toPrimitive(input, hint) { if (CandidateBox_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (CandidateBox_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }


var CandidateBox = /*#__PURE__*/function () {
  function CandidateBox(_ref) {
    var utilities = _ref.utilities,
      options = _ref.options;
    CandidateBox_classCallCheck(this, CandidateBox);
    CandidateBox_defineProperty(this, "utilities", void 0);
    CandidateBox_defineProperty(this, "options", void 0);
    CandidateBox_defineProperty(this, "candidateBoxElement", void 0);
    CandidateBox_defineProperty(this, "pageIndex", 0);
    CandidateBox_defineProperty(this, "pageSize", void 0);
    this.utilities = utilities;
    this.options = options;
    services_Utilities.bindMethods(CandidateBox, this);
    this.pageSize = this.utilities.getOptions().layoutCandidatesPageSize || 5;
  }
  CandidateBox_createClass(CandidateBox, [{
    key: "destroy",
    value: function destroy() {
      if (this.candidateBoxElement) {
        this.candidateBoxElement.remove();
        this.pageIndex = 0;
      }
    }
  }, {
    key: "show",
    value: function show(_ref2) {
      var _this = this;
      var candidateValue = _ref2.candidateValue,
        targetElement = _ref2.targetElement,
        onSelect = _ref2.onSelect;
      if (!candidateValue || !candidateValue.length) {
        return;
      }
      var candidateListPages = this.utilities.chunkArray(candidateValue.split(" "), this.pageSize);
      this.renderPage({
        candidateListPages: candidateListPages,
        targetElement: targetElement,
        pageIndex: this.pageIndex,
        nbPages: candidateListPages.length,
        onItemSelected: function onItemSelected(selectedCandidate, e) {
          onSelect(selectedCandidate, e);
          _this.destroy();
        }
      });
    }
  }, {
    key: "renderPage",
    value: function renderPage(_ref3) {
      var _this$candidateBoxEle,
        _this2 = this;
      var candidateListPages = _ref3.candidateListPages,
        targetElement = _ref3.targetElement,
        pageIndex = _ref3.pageIndex,
        nbPages = _ref3.nbPages,
        onItemSelected = _ref3.onItemSelected;
      // Remove current candidate box, if any
      (_this$candidateBoxEle = this.candidateBoxElement) === null || _this$candidateBoxEle === void 0 || _this$candidateBoxEle.remove();

      // Create candidate box element
      this.candidateBoxElement = document.createElement("div");
      this.candidateBoxElement.className = "hg-candidate-box";

      // Candidate box list
      var candidateListULElement = document.createElement("ul");
      candidateListULElement.className = "hg-candidate-box-list";

      // Create Candidate box list items
      candidateListPages[pageIndex].forEach(function (candidateListItem) {
        var _this2$options$displa;
        var candidateListLIElement = document.createElement("li");
        var getMouseEvent = function getMouseEvent() {
          var mouseEvent = new (_this2.options.useTouchEvents ? TouchEvent : MouseEvent)("click");
          Object.defineProperty(mouseEvent, "target", {
            value: candidateListLIElement
          });
          return mouseEvent;
        };
        candidateListLIElement.className = "hg-candidate-box-list-item";
        candidateListLIElement.innerHTML = ((_this2$options$displa = _this2.options.display) === null || _this2$options$displa === void 0 ? void 0 : _this2$options$displa[candidateListItem]) || candidateListItem;
        if (_this2.options.useTouchEvents) {
          candidateListLIElement.ontouchstart = function (e) {
            return onItemSelected(candidateListItem, e || getMouseEvent());
          };
        } else {
          candidateListLIElement.onclick = function () {
            var e = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : getMouseEvent();
            return onItemSelected(candidateListItem, e);
          };
        }

        // Append list item to ul
        candidateListULElement.appendChild(candidateListLIElement);
      });

      // Add previous button
      var isPrevBtnElementActive = pageIndex > 0;
      var prevBtnElement = document.createElement("div");
      prevBtnElement.classList.add("hg-candidate-box-prev");
      isPrevBtnElementActive && prevBtnElement.classList.add("hg-candidate-box-btn-active");
      var prevBtnElementClickAction = function prevBtnElementClickAction() {
        if (!isPrevBtnElementActive) return;
        _this2.renderPage({
          candidateListPages: candidateListPages,
          targetElement: targetElement,
          pageIndex: pageIndex - 1,
          nbPages: nbPages,
          onItemSelected: onItemSelected
        });
      };
      if (this.options.useTouchEvents) {
        prevBtnElement.ontouchstart = prevBtnElementClickAction;
      } else {
        prevBtnElement.onclick = prevBtnElementClickAction;
      }
      this.candidateBoxElement.appendChild(prevBtnElement);

      // Add elements to container
      this.candidateBoxElement.appendChild(candidateListULElement);

      // Add next button
      var isNextBtnElementActive = pageIndex < nbPages - 1;
      var nextBtnElement = document.createElement("div");
      nextBtnElement.classList.add("hg-candidate-box-next");
      isNextBtnElementActive && nextBtnElement.classList.add("hg-candidate-box-btn-active");
      var nextBtnElementClickAction = function nextBtnElementClickAction() {
        if (!isNextBtnElementActive) return;
        _this2.renderPage({
          candidateListPages: candidateListPages,
          targetElement: targetElement,
          pageIndex: pageIndex + 1,
          nbPages: nbPages,
          onItemSelected: onItemSelected
        });
      };
      if (this.options.useTouchEvents) {
        nextBtnElement.ontouchstart = nextBtnElementClickAction;
      } else {
        nextBtnElement.onclick = nextBtnElementClickAction;
      }
      this.candidateBoxElement.appendChild(nextBtnElement);

      // Append candidate box to target element
      targetElement.prepend(this.candidateBoxElement);
    }
  }]);
  return CandidateBox;
}();
/* harmony default export */ const components_CandidateBox = (CandidateBox);
;// CONCATENATED MODULE: ./src/lib/components/Keyboard.ts
function Keyboard_toConsumableArray(arr) { return Keyboard_arrayWithoutHoles(arr) || Keyboard_iterableToArray(arr) || Keyboard_unsupportedIterableToArray(arr) || Keyboard_nonIterableSpread(); }
function Keyboard_nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function Keyboard_unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return Keyboard_arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return Keyboard_arrayLikeToArray(o, minLen); }
function Keyboard_iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }
function Keyboard_arrayWithoutHoles(arr) { if (Array.isArray(arr)) return Keyboard_arrayLikeToArray(arr); }
function Keyboard_arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }
function Keyboard_typeof(o) { "@babel/helpers - typeof"; return Keyboard_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, Keyboard_typeof(o); }
function ownKeys(e, r) { var t = Object.keys(e); if (Object.getOwnPropertySymbols) { var o = Object.getOwnPropertySymbols(e); r && (o = o.filter(function (r) { return Object.getOwnPropertyDescriptor(e, r).enumerable; })), t.push.apply(t, o); } return t; }
function _objectSpread(e) { for (var r = 1; r < arguments.length; r++) { var t = null != arguments[r] ? arguments[r] : {}; r % 2 ? ownKeys(Object(t), !0).forEach(function (r) { Keyboard_defineProperty(e, r, t[r]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function (r) { Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r)); }); } return e; }
function Keyboard_classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function Keyboard_defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, Keyboard_toPropertyKey(descriptor.key), descriptor); } }
function Keyboard_createClass(Constructor, protoProps, staticProps) { if (protoProps) Keyboard_defineProperties(Constructor.prototype, protoProps); if (staticProps) Keyboard_defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function Keyboard_defineProperty(obj, key, value) { key = Keyboard_toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function Keyboard_toPropertyKey(arg) { var key = Keyboard_toPrimitive(arg, "string"); return Keyboard_typeof(key) === "symbol" ? key : String(key); }
function Keyboard_toPrimitive(input, hint) { if (Keyboard_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (Keyboard_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }


// Services





/**
 * Root class for simple-keyboard.
 * This class:
 * - Parses the options
 * - Renders the rows and buttons
 * - Handles button functionality
 */
var SimpleKeyboard = /*#__PURE__*/function () {
  /**
   * Creates an instance of SimpleKeyboard
   * @param {Array} params If first parameter is a string, it is considered the container class. The second parameter is then considered the options object. If first parameter is an object, it is considered the options object.
   */
  function SimpleKeyboard(_selectorOrOptions, _keyboardOptions) {
    var _this = this;
    Keyboard_classCallCheck(this, SimpleKeyboard);
    Keyboard_defineProperty(this, "input", void 0);
    Keyboard_defineProperty(this, "options", void 0);
    Keyboard_defineProperty(this, "utilities", void 0);
    Keyboard_defineProperty(this, "caretPosition", void 0);
    Keyboard_defineProperty(this, "caretPositionEnd", void 0);
    Keyboard_defineProperty(this, "keyboardDOM", void 0);
    Keyboard_defineProperty(this, "keyboardPluginClasses", void 0);
    Keyboard_defineProperty(this, "keyboardDOMClass", void 0);
    Keyboard_defineProperty(this, "buttonElements", void 0);
    Keyboard_defineProperty(this, "currentInstanceName", void 0);
    Keyboard_defineProperty(this, "allKeyboardInstances", void 0);
    Keyboard_defineProperty(this, "keyboardInstanceNames", void 0);
    Keyboard_defineProperty(this, "isFirstKeyboardInstance", void 0);
    Keyboard_defineProperty(this, "physicalKeyboard", void 0);
    Keyboard_defineProperty(this, "modules", void 0);
    Keyboard_defineProperty(this, "activeButtonClass", void 0);
    Keyboard_defineProperty(this, "holdInteractionTimeout", void 0);
    Keyboard_defineProperty(this, "holdTimeout", void 0);
    Keyboard_defineProperty(this, "isMouseHold", void 0);
    Keyboard_defineProperty(this, "initialized", void 0);
    Keyboard_defineProperty(this, "candidateBox", void 0);
    Keyboard_defineProperty(this, "keyboardRowsDOM", void 0);
    Keyboard_defineProperty(this, "defaultName", "default");
    Keyboard_defineProperty(this, "activeInputElement", null);
    /**
     * parseParams
     */
    Keyboard_defineProperty(this, "handleParams", function (selectorOrOptions, keyboardOptions) {
      var keyboardDOMClass;
      var keyboardDOM;
      var options;

      /**
       * If first parameter is a string:
       * Consider it as an element's class
       */
      if (typeof selectorOrOptions === "string") {
        keyboardDOMClass = selectorOrOptions.split(".").join("");
        keyboardDOM = document.querySelector(".".concat(keyboardDOMClass));
        options = keyboardOptions;

        /**
         * If first parameter is an KeyboardElement
         * Consider it as the keyboard DOM element
         */
      } else if (selectorOrOptions instanceof HTMLDivElement) {
        /**
         * This element must have a class, otherwise throw
         */
        if (!selectorOrOptions.className) {
          console.warn("Any DOM element passed as parameter must have a class.");
          throw new Error("KEYBOARD_DOM_CLASS_ERROR");
        }
        keyboardDOMClass = selectorOrOptions.className.split(" ")[0];
        keyboardDOM = selectorOrOptions;
        options = keyboardOptions;

        /**
         * Otherwise, search for .simple-keyboard DOM element
         */
      } else {
        keyboardDOMClass = "simple-keyboard";
        keyboardDOM = document.querySelector(".".concat(keyboardDOMClass));
        options = selectorOrOptions;
      }
      return {
        keyboardDOMClass: keyboardDOMClass,
        keyboardDOM: keyboardDOM,
        options: options
      };
    });
    /**
     * Getters
     */
    Keyboard_defineProperty(this, "getOptions", function () {
      return _this.options;
    });
    Keyboard_defineProperty(this, "getCaretPosition", function () {
      return _this.caretPosition;
    });
    Keyboard_defineProperty(this, "getCaretPositionEnd", function () {
      return _this.caretPositionEnd;
    });
    /**
     * Register module
     */
    Keyboard_defineProperty(this, "registerModule", function (name, initCallback) {
      if (!_this.modules[name]) _this.modules[name] = {};
      initCallback(_this.modules[name]);
    });
    /**
     * getKeyboardClassString
     */
    Keyboard_defineProperty(this, "getKeyboardClassString", function () {
      for (var _len = arguments.length, baseDOMClasses = new Array(_len), _key = 0; _key < _len; _key++) {
        baseDOMClasses[_key] = arguments[_key];
      }
      var keyboardClasses = [_this.keyboardDOMClass].concat(baseDOMClasses).filter(function (DOMClass) {
        return !!DOMClass;
      });
      return keyboardClasses.join(" ");
    });
    if (typeof window === "undefined") return;
    var _this$handleParams = this.handleParams(_selectorOrOptions, _keyboardOptions),
      _keyboardDOMClass = _this$handleParams.keyboardDOMClass,
      _keyboardDOM = _this$handleParams.keyboardDOM,
      _this$handleParams$op = _this$handleParams.options,
      _options = _this$handleParams$op === void 0 ? {} : _this$handleParams$op;

    /**
     * Initializing Utilities
     */
    this.utilities = new services_Utilities({
      getOptions: this.getOptions,
      getCaretPosition: this.getCaretPosition,
      getCaretPositionEnd: this.getCaretPositionEnd,
      dispatch: this.dispatch
    });

    /**
     * Caret position
     */
    this.caretPosition = null;

    /**
     * Caret position end
     */
    this.caretPositionEnd = null;

    /**
     * Processing options
     */
    this.keyboardDOM = _keyboardDOM;

    /**
     * @type {object}
     * @property {object} layout Modify the keyboard layout.
     * @property {string} layoutName Specifies which layout should be used.
     * @property {object} display Replaces variable buttons (such as {bksp}) with a human-friendly name (e.g.: “backspace”).
     * @property {boolean} mergeDisplay By default, when you set the display property, you replace the default one. This setting merges them instead.
     * @property {string} theme A prop to add your own css classes to the keyboard wrapper. You can add multiple classes separated by a space.
     * @property {array} buttonTheme A prop to add your own css classes to one or several buttons.
     * @property {array} buttonAttributes A prop to add your own attributes to one or several buttons.
     * @property {boolean} debug Runs a console.log every time a key is pressed. Displays the buttons pressed and the current input.
     * @property {boolean} newLineOnEnter Specifies whether clicking the “ENTER” button will input a newline (\n) or not.
     * @property {boolean} tabCharOnTab Specifies whether clicking the “TAB” button will input a tab character (\t) or not.
     * @property {string} inputName Allows you to use a single simple-keyboard instance for several inputs.
     * @property {number} maxLength Restrains all of simple-keyboard inputs to a certain length. This should be used in addition to the input element’s maxlengthattribute.
     * @property {object} maxLength Restrains simple-keyboard’s individual inputs to a certain length. This should be used in addition to the input element’s maxlengthattribute.
     * @property {boolean} syncInstanceInputs When set to true, this option synchronizes the internal input of every simple-keyboard instance.
     * @property {boolean} physicalKeyboardHighlight Enable highlighting of keys pressed on physical keyboard.
     * @property {boolean} physicalKeyboardHighlightPress Presses keys highlighted by physicalKeyboardHighlight
     * @property {string} physicalKeyboardHighlightTextColor Define the text color that the physical keyboard highlighted key should have.
     * @property {string} physicalKeyboardHighlightBgColor Define the background color that the physical keyboard highlighted key should have.
     * @property {boolean} physicalKeyboardHighlightPressUseClick Whether physicalKeyboardHighlightPress should use clicks to trigger buttons.
     * @property {boolean} physicalKeyboardHighlightPressUsePointerEvents Whether physicalKeyboardHighlightPress should use pointer events to trigger buttons.
     * @property {boolean} physicalKeyboardHighlightPreventDefault Whether physicalKeyboardHighlight should use preventDefault to disable default browser actions.
     * @property {boolean} preventMouseDownDefault Calling preventDefault for the mousedown events keeps the focus on the input.
     * @property {boolean} preventMouseUpDefault Calling preventDefault for the mouseup events.
     * @property {boolean} stopMouseDownPropagation Stops pointer down events on simple-keyboard buttons from bubbling to parent elements.
     * @property {boolean} stopMouseUpPropagation Stops pointer up events on simple-keyboard buttons from bubbling to parent elements.
     * @property {function(button: string):string} onKeyPress Executes the callback function on key press. Returns button layout name (i.e.: “{shift}”).
     * @property {function(input: string):string} onChange Executes the callback function on input change. Returns the current input’s string.
     * @property {function} onRender Executes the callback function every time simple-keyboard is rendered (e.g: when you change layouts).
     * @property {function} onInit Executes the callback function once simple-keyboard is rendered for the first time (on initialization).
     * @property {function(inputs: object):object} onChangeAll Executes the callback function on input change. Returns the input object with all defined inputs.
     * @property {boolean} useButtonTag Render buttons as a button element instead of a div element.
     * @property {boolean} disableCaretPositioning A prop to ensure characters are always be added/removed at the end of the string.
     * @property {object} inputPattern Restrains input(s) change to the defined regular expression pattern.
     * @property {boolean} useTouchEvents Instructs simple-keyboard to use touch events instead of click events.
     * @property {boolean} autoUseTouchEvents Enable useTouchEvents automatically when touch device is detected.
     * @property {boolean} useMouseEvents Opt out of PointerEvents handling, falling back to the prior mouse event logic.
     * @property {function} destroy Clears keyboard listeners and DOM elements.
     * @property {boolean} disableButtonHold Disable button hold action.
     * @property {boolean} rtl Adds unicode right-to-left control characters to input return values.
     * @property {function} onKeyReleased Executes the callback function on key release.
     * @property {array} modules Module classes to be loaded by simple-keyboard.
     * @property {boolean} enableLayoutCandidates Enable input method editor candidate list support.
     * @property {object} excludeFromLayout Buttons to exclude from layout
     * @property {number} layoutCandidatesPageSize Determines size of layout candidate list
     * @property {boolean} layoutCandidatesCaseSensitiveMatch Determines whether layout candidate match should be case sensitive.
     * @property {boolean} disableCandidateNormalization Disables the automatic normalization for selected layout candidates
     * @property {boolean} enableLayoutCandidatesKeyPress Enables onKeyPress triggering for layoutCandidate items
     */
    this.options = _objectSpread({
      layoutName: "default",
      theme: "hg-theme-default",
      inputName: "default",
      preventMouseDownDefault: false,
      enableLayoutCandidates: true,
      excludeFromLayout: {}
    }, _options);

    /**
     * @type {object} Classes identifying loaded plugins
     */
    this.keyboardPluginClasses = "";

    /**
     * Bindings
     */
    services_Utilities.bindMethods(SimpleKeyboard, this);

    /**
     * simple-keyboard uses a non-persistent internal input to keep track of the entered string (the variable `keyboard.input`).
     * This removes any dependency to input DOM elements. You can type and directly display the value in a div element, for example.
     * @example
     * // To get entered input
     * const input = keyboard.getInput();
     *
     * // To clear entered input.
     * keyboard.clearInput();
     *
     * @type {object}
     * @property {object} default Default SimpleKeyboard internal input.
     * @property {object} myInputName Example input that can be set through `options.inputName:"myInputName"`.
     */
    var _this$options$inputNa = this.options.inputName,
      inputName = _this$options$inputNa === void 0 ? this.defaultName : _this$options$inputNa;
    this.input = {};
    this.input[inputName] = "";

    /**
     * @type {string} DOM class of the keyboard wrapper, normally "simple-keyboard" by default.
     */
    this.keyboardDOMClass = _keyboardDOMClass;

    /**
     * @type {object} Contains the DOM elements of every rendered button, the key being the button's layout name (e.g.: "{enter}").
     */
    this.buttonElements = {};

    /**
     * Simple-keyboard Instances
     * This enables multiple simple-keyboard support with easier management
     */
    if (!window["SimpleKeyboardInstances"]) window["SimpleKeyboardInstances"] = {};
    this.currentInstanceName = this.utilities.camelCase(this.keyboardDOMClass);
    window["SimpleKeyboardInstances"][this.currentInstanceName] = this;

    /**
     * Instance vars
     */
    this.allKeyboardInstances = window["SimpleKeyboardInstances"];
    this.keyboardInstanceNames = Object.keys(window["SimpleKeyboardInstances"]);
    this.isFirstKeyboardInstance = this.keyboardInstanceNames[0] === this.currentInstanceName;

    /**
     * Physical Keyboard support
     */
    this.physicalKeyboard = new services_PhysicalKeyboard({
      dispatch: this.dispatch,
      getOptions: this.getOptions
    });

    /**
     * Initializing CandidateBox
     */
    this.candidateBox = this.options.enableLayoutCandidates ? new components_CandidateBox({
      utilities: this.utilities,
      options: this.options
    }) : null;

    /**
     * Rendering keyboard
     */
    if (this.keyboardDOM) this.render();else {
      console.warn("\".".concat(_keyboardDOMClass, "\" was not found in the DOM."));
      throw new Error("KEYBOARD_DOM_ERROR");
    }

    /**
     * Modules
     */
    this.modules = {};
    this.loadModules();
  }
  Keyboard_createClass(SimpleKeyboard, [{
    key: "setCaretPosition",
    value:
    /**
     * Changes the internal caret position
     * @param {number} position The caret's start position
     * @param {number} positionEnd The caret's end position
     */
    function setCaretPosition(position) {
      var endPosition = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : position;
      this.caretPosition = position;
      this.caretPositionEnd = endPosition;
    }

    /**
     * Retrieve the candidates for a given input
     * @param input The input string to check
     */
  }, {
    key: "getInputCandidates",
    value: function getInputCandidates(input) {
      var _this2 = this;
      var _this$options = this.options,
        layoutCandidatesObj = _this$options.layoutCandidates,
        layoutCandidatesCaseSensitiveMatch = _this$options.layoutCandidatesCaseSensitiveMatch;
      if (!layoutCandidatesObj || Keyboard_typeof(layoutCandidatesObj) !== "object") {
        return {};
      }
      var layoutCandidates = Object.keys(layoutCandidatesObj).filter(function (layoutCandidate) {
        var inputSubstr = input.substring(0, _this2.getCaretPositionEnd() || 0) || input;
        var regexp = new RegExp("".concat(_this2.utilities.escapeRegex(layoutCandidate), "$"), layoutCandidatesCaseSensitiveMatch ? "g" : "gi");
        var matches = Keyboard_toConsumableArray(inputSubstr.matchAll(regexp));
        return !!matches.length;
      });
      if (layoutCandidates.length > 1) {
        var candidateKey = layoutCandidates.sort(function (a, b) {
          return b.length - a.length;
        })[0];
        return {
          candidateKey: candidateKey,
          candidateValue: layoutCandidatesObj[candidateKey]
        };
      } else if (layoutCandidates.length) {
        var _candidateKey = layoutCandidates[0];
        return {
          candidateKey: _candidateKey,
          candidateValue: layoutCandidatesObj[_candidateKey]
        };
      } else {
        return {};
      }
    }

    /**
     * Shows a suggestion box with a list of candidate words
     * @param candidates The chosen candidates string as defined in the layoutCandidates option
     * @param targetElement The element next to which the candidates box will be shown
     */
  }, {
    key: "showCandidatesBox",
    value: function showCandidatesBox(candidateKey, candidateValue, targetElement) {
      var _this3 = this;
      if (this.candidateBox) {
        this.candidateBox.show({
          candidateValue: candidateValue,
          targetElement: targetElement,
          onSelect: function onSelect(selectedCandidate, e) {
            var _this3$options = _this3.options,
              layoutCandidatesCaseSensitiveMatch = _this3$options.layoutCandidatesCaseSensitiveMatch,
              disableCandidateNormalization = _this3$options.disableCandidateNormalization,
              enableLayoutCandidatesKeyPress = _this3$options.enableLayoutCandidatesKeyPress;
            var candidateStr = selectedCandidate;
            if (!disableCandidateNormalization) {
              /**
               * Making sure that our suggestions are not composed characters
               */
              candidateStr = selectedCandidate.normalize("NFD");
            }
            var currentInput = _this3.getInput(_this3.options.inputName, true);
            var initialCaretPosition = _this3.getCaretPositionEnd() || 0;
            var inputSubstr = currentInput.substring(0, initialCaretPosition || 0) || currentInput;
            var regexp = new RegExp("".concat(_this3.utilities.escapeRegex(candidateKey), "$"), layoutCandidatesCaseSensitiveMatch ? "g" : "gi");
            var newInputSubstr = inputSubstr.replace(regexp, candidateStr);
            var newInput = currentInput.replace(inputSubstr, newInputSubstr);
            var caretPositionDiff = newInputSubstr.length - inputSubstr.length;
            var newCaretPosition = (initialCaretPosition || currentInput.length) + caretPositionDiff;
            if (newCaretPosition < 0) newCaretPosition = 0;
            _this3.setInput(newInput, _this3.options.inputName, true);
            _this3.setCaretPosition(newCaretPosition);

            /**
             * Calling onKeyPress
             * We pass in the composed candidate instead of the decomposed one
             * To prevent confusion for users
             */
            if (enableLayoutCandidatesKeyPress && typeof _this3.options.onKeyPress === "function") _this3.options.onKeyPress(selectedCandidate, e);
            if (typeof _this3.options.onChange === "function") _this3.options.onChange(_this3.getInput(_this3.options.inputName, true), e);

            /**
             * Calling onChangeAll
             */
            if (typeof _this3.options.onChangeAll === "function") _this3.options.onChangeAll(_this3.getAllInputs(), e);
          }
        });
      }
    }

    /**
     * Handles clicks made to keyboard buttons
     * @param  {string} button The button's layout name.
     */
  }, {
    key: "handleButtonClicked",
    value: function handleButtonClicked(button, e) {
      var _this$options2 = this.options,
        _this$options2$inputN = _this$options2.inputName,
        inputName = _this$options2$inputN === void 0 ? this.defaultName : _this$options2$inputN,
        debug = _this$options2.debug;
      /**
       * Ignoring placeholder buttons
       */
      if (button === "{//}") return;

      /**
       * Creating inputName if it doesn't exist
       */
      if (!this.input[inputName]) this.input[inputName] = "";

      /**
       * Calculating new input
       */
      var updatedInput = this.utilities.getUpdatedInput(button, this.input[inputName], this.caretPosition, this.caretPositionEnd);

      /**
       * EDGE CASE: Check for whole input selection changes that will yield same updatedInput
       */
      if (this.utilities.isStandardButton(button) && this.activeInputElement) {
        var isEntireInputSelection = this.input[inputName] && this.input[inputName] === updatedInput && this.caretPosition === 0 && this.caretPositionEnd === updatedInput.length;
        if (isEntireInputSelection) {
          this.setInput("", this.options.inputName, true);
          this.setCaretPosition(0);
          this.activeInputElement.value = "";
          this.activeInputElement.setSelectionRange(0, 0);
          this.handleButtonClicked(button, e);
          return;
        }
      }

      /**
       * Calling onKeyPress
       */
      if (typeof this.options.onKeyPress === "function") this.options.onKeyPress(button, e);
      if (
      // If input will change as a result of this button press
      this.input[inputName] !== updatedInput && (
      // This pertains to the "inputPattern" option:
      // If inputPattern isn't set
      !this.options.inputPattern ||
      // Or, if it is set and if the pattern is valid - we proceed.
      this.options.inputPattern && this.inputPatternIsValid(updatedInput))) {
        /**
         * If maxLength and handleMaxLength yield true, halting
         */
        if (this.options.maxLength && this.utilities.handleMaxLength(this.input, updatedInput)) {
          return;
        }

        /**
         * Updating input
         */
        var newInputValue = this.utilities.getUpdatedInput(button, this.input[inputName], this.caretPosition, this.caretPositionEnd, true);
        this.setInput(newInputValue, this.options.inputName, true);
        if (debug) console.log("Input changed:", this.getAllInputs());
        if (this.options.debug) {
          console.log("Caret at: ", this.getCaretPosition(), this.getCaretPositionEnd(), "(".concat(this.keyboardDOMClass, ")"), e === null || e === void 0 ? void 0 : e.type);
        }

        /**
         * Enforce syncInstanceInputs, if set
         */
        if (this.options.syncInstanceInputs) this.syncInstanceInputs();

        /**
         * Calling onChange
         */
        if (typeof this.options.onChange === "function") this.options.onChange(this.getInput(this.options.inputName, true), e);

        /**
         * Calling onChangeAll
         */
        if (typeof this.options.onChangeAll === "function") this.options.onChangeAll(this.getAllInputs(), e);

        /**
         * Check if this new input has candidates (suggested words)
         */
        if (e !== null && e !== void 0 && e.target && this.options.enableLayoutCandidates) {
          var _this$getInputCandida = this.getInputCandidates(updatedInput),
            candidateKey = _this$getInputCandida.candidateKey,
            candidateValue = _this$getInputCandida.candidateValue;
          if (candidateKey && candidateValue) {
            this.showCandidatesBox(candidateKey, candidateValue, this.keyboardDOM);
          } else {
            var _this$candidateBox;
            (_this$candidateBox = this.candidateBox) === null || _this$candidateBox === void 0 || _this$candidateBox.destroy();
          }
        }
      }

      /**
       * After a button is clicked the selection (if any) will disappear
       * we should reflect this in our state, as applicable
       */
      if (this.caretPositionEnd && this.caretPosition !== this.caretPositionEnd) {
        this.setCaretPosition(this.caretPositionEnd, this.caretPositionEnd);
        if (this.activeInputElement) {
          this.activeInputElement.setSelectionRange(this.caretPositionEnd, this.caretPositionEnd);
        }
        if (this.options.debug) {
          console.log("Caret position aligned", this.caretPosition);
        }
      }
      if (debug) {
        console.log("Key pressed:", button);
      }
    }

    /**
     * Get mouse hold state
     */
  }, {
    key: "getMouseHold",
    value: function getMouseHold() {
      return this.isMouseHold;
    }

    /**
     * Mark mouse hold state as set
     */
  }, {
    key: "setMouseHold",
    value: function setMouseHold(value) {
      if (this.options.syncInstanceInputs) {
        this.dispatch(function (instance) {
          instance.isMouseHold = value;
        });
      } else {
        this.isMouseHold = value;
      }
    }

    /**
     * Handles button mousedown
     */
    /* istanbul ignore next */
  }, {
    key: "handleButtonMouseDown",
    value: function handleButtonMouseDown(button, e) {
      var _this4 = this;
      if (e) {
        /**
         * Handle event options
         */
        if (this.options.preventMouseDownDefault) e.preventDefault();
        if (this.options.stopMouseDownPropagation) e.stopPropagation();

        /**
         * Add active class
         */
        e.target.classList.add(this.activeButtonClass);
      }
      if (this.holdInteractionTimeout) clearTimeout(this.holdInteractionTimeout);
      if (this.holdTimeout) clearTimeout(this.holdTimeout);

      /**
       * @type {boolean} Whether the mouse is being held onKeyPress
       */
      this.setMouseHold(true);

      /**
       * @type {object} Time to wait until a key hold is detected
       */
      if (!this.options.disableButtonHold) {
        this.holdTimeout = window.setTimeout(function () {
          if (_this4.getMouseHold() && (
          // TODO: This needs to be configurable through options
          !button.includes("{") && !button.includes("}") || button === "{delete}" || button === "{backspace}" || button === "{bksp}" || button === "{space}" || button === "{tab}") || button === "{arrowright}" || button === "{arrowleft}" || button === "{arrowup}" || button === "{arrowdown}") {
            if (_this4.options.debug) console.log("Button held:", button);
            _this4.handleButtonHold(button);
          }
          clearTimeout(_this4.holdTimeout);
        }, 500);
      }
    }

    /**
     * Handles button mouseup
     */
  }, {
    key: "handleButtonMouseUp",
    value: function handleButtonMouseUp(button, e) {
      var _this5 = this;
      if (e) {
        /**
         * Handle event options
         */
        if (this.options.preventMouseUpDefault && e.preventDefault) e.preventDefault();
        if (this.options.stopMouseUpPropagation && e.stopPropagation) e.stopPropagation();

        /* istanbul ignore next */
        var isKeyboard = e.target === this.keyboardDOM || e.target && this.keyboardDOM.contains(e.target) || this.candidateBox && this.candidateBox.candidateBoxElement && (e.target === this.candidateBox.candidateBoxElement || e.target && this.candidateBox.candidateBoxElement.contains(e.target));

        /**
         * On click outside, remove candidateBox
         */
        if (!isKeyboard && this.candidateBox) {
          this.candidateBox.destroy();
        }
      }

      /**
       * Remove active class
       */
      this.recurseButtons(function (buttonElement) {
        buttonElement.classList.remove(_this5.activeButtonClass);
      });
      this.setMouseHold(false);
      if (this.holdInteractionTimeout) clearTimeout(this.holdInteractionTimeout);

      /**
       * Calling onKeyReleased
       */
      if (button && typeof this.options.onKeyReleased === "function") this.options.onKeyReleased(button, e);
    }

    /**
     * Handles container mousedown
     */
  }, {
    key: "handleKeyboardContainerMouseDown",
    value: function handleKeyboardContainerMouseDown(e) {
      /**
       * Handle event options
       */
      if (this.options.preventMouseDownDefault) e.preventDefault();
    }

    /**
     * Handles button hold
     */
    /* istanbul ignore next */
  }, {
    key: "handleButtonHold",
    value: function handleButtonHold(button) {
      var _this6 = this;
      if (this.holdInteractionTimeout) clearTimeout(this.holdInteractionTimeout);

      /**
       * @type {object} Timeout dictating the speed of key hold iterations
       */
      this.holdInteractionTimeout = window.setTimeout(function () {
        if (_this6.getMouseHold()) {
          _this6.handleButtonClicked(button);
          _this6.handleButtonHold(button);
        } else {
          clearTimeout(_this6.holdInteractionTimeout);
        }
      }, 100);
    }

    /**
     * Send a command to all simple-keyboard instances (if you have several instances).
     */
  }, {
    key: "syncInstanceInputs",
    value: function syncInstanceInputs() {
      var _this7 = this;
      this.dispatch(function (instance) {
        instance.replaceInput(_this7.input);
        instance.setCaretPosition(_this7.caretPosition, _this7.caretPositionEnd);
      });
    }

    /**
     * Clear the keyboard’s input.
     * @param {string} [inputName] optional - the internal input to select
     */
  }, {
    key: "clearInput",
    value: function clearInput() {
      var inputName = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.options.inputName || this.defaultName;
      this.input[inputName] = "";

      /**
       * Reset caretPosition
       */
      this.setCaretPosition(0);

      /**
       * Enforce syncInstanceInputs, if set
       */
      if (this.options.syncInstanceInputs) this.syncInstanceInputs();
    }

    /**
     * Get the keyboard’s input (You can also get it from the onChange prop).
     * @param  {string} [inputName] optional - the internal input to select
     */
  }, {
    key: "getInput",
    value: function getInput() {
      var inputName = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : this.options.inputName || this.defaultName;
      var skipSync = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;
      /**
       * Enforce syncInstanceInputs, if set
       */
      if (this.options.syncInstanceInputs && !skipSync) this.syncInstanceInputs();
      if (this.options.rtl) {
        // Remove existing control chars
        var inputWithoutRTLControl = this.input[inputName].replace("\u202B", "").replace("\u202C", "");
        return "\u202B" + inputWithoutRTLControl + "\u202C";
      } else {
        return this.input[inputName];
      }
    }

    /**
     * Get all simple-keyboard inputs
     */
  }, {
    key: "getAllInputs",
    value: function getAllInputs() {
      var _this8 = this;
      var output = {};
      var inputNames = Object.keys(this.input);
      inputNames.forEach(function (inputName) {
        output[inputName] = _this8.getInput(inputName, true);
      });
      return output;
    }

    /**
     * Set the keyboard’s input.
     * @param  {string} input the input value
     * @param  {string} inputName optional - the internal input to select
     */
  }, {
    key: "setInput",
    value: function setInput(input) {
      var inputName = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.options.inputName || this.defaultName;
      var skipSync = arguments.length > 2 ? arguments[2] : undefined;
      this.input[inputName] = input;

      /**
       * Enforce syncInstanceInputs, if set
       */
      if (!skipSync && this.options.syncInstanceInputs) this.syncInstanceInputs();
    }

    /**
     * Replace the input object (`keyboard.input`)
     * @param  {object} inputObj The input object
     */
  }, {
    key: "replaceInput",
    value: function replaceInput(inputObj) {
      this.input = inputObj;
    }

    /**
     * Set new option or modify existing ones after initialization.
     * @param  {object} options The options to set
     */
  }, {
    key: "setOptions",
    value: function setOptions() {
      var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      var changedOptions = this.changedOptions(options);
      this.options = Object.assign(this.options, options);
      if (changedOptions.length) {
        if (this.options.debug) {
          console.log("changedOptions", changedOptions);
        }

        /**
         * Some option changes require adjustments before re-render
         */
        this.onSetOptions(changedOptions);

        /**
         * Rendering
         */
        this.render();
      }
    }

    /**
     * Detecting changes to non-function options
     * This allows us to ascertain whether a button re-render is needed
     */
  }, {
    key: "changedOptions",
    value: function changedOptions(newOptions) {
      var _this9 = this;
      return Object.keys(newOptions).filter(function (optionName) {
        return JSON.stringify(newOptions[optionName]) !== JSON.stringify(_this9.options[optionName]);
      });
    }

    /**
     * Executing actions depending on changed options
     * @param  {object} options The options to set
     */
  }, {
    key: "onSetOptions",
    value: function onSetOptions() {
      var changedOptions = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
      /**
       * Changed: layoutName
       */
      if (changedOptions.includes("layoutName")) {
        /**
         * Reset candidateBox
         */
        if (this.candidateBox) {
          this.candidateBox.destroy();
        }
      }

      /**
       * Changed: layoutCandidatesPageSize, layoutCandidates
       */
      if (changedOptions.includes("layoutCandidatesPageSize") || changedOptions.includes("layoutCandidates")) {
        /**
         * Reset and recreate candidateBox
         */
        if (this.candidateBox) {
          this.candidateBox.destroy();
          this.candidateBox = new components_CandidateBox({
            utilities: this.utilities,
            options: this.options
          });
        }
      }
    }

    /**
     * Remove all keyboard rows and reset keyboard values.
     * Used internally between re-renders.
     */
  }, {
    key: "resetRows",
    value: function resetRows() {
      if (this.keyboardRowsDOM) {
        this.keyboardRowsDOM.remove();
      }
      this.keyboardDOM.className = this.keyboardDOMClass;
      this.keyboardDOM.setAttribute("data-skInstance", this.currentInstanceName);
      this.buttonElements = {};
    }

    /**
     * Send a command to all simple-keyboard instances at once (if you have multiple instances).
     * @param  {function(instance: object, key: string)} callback Function to run on every instance
     */
    // eslint-disable-next-line no-unused-vars
  }, {
    key: "dispatch",
    value: function dispatch(callback) {
      if (!window["SimpleKeyboardInstances"]) {
        console.warn("SimpleKeyboardInstances is not defined. Dispatch cannot be called.");
        throw new Error("INSTANCES_VAR_ERROR");
      }
      return Object.keys(window["SimpleKeyboardInstances"]).forEach(function (key) {
        callback(window["SimpleKeyboardInstances"][key], key);
      });
    }

    /**
     * Adds/Modifies an entry to the `buttonTheme`. Basically a way to add a class to a button.
     * @param  {string} buttons List of buttons to select (separated by a space).
     * @param  {string} className Classes to give to the selected buttons (separated by space).
     */
  }, {
    key: "addButtonTheme",
    value: function addButtonTheme(buttons, className) {
      var _this10 = this;
      if (!className || !buttons) return;
      buttons.split(" ").forEach(function (button) {
        className.split(" ").forEach(function (classNameItem) {
          if (!_this10.options.buttonTheme) _this10.options.buttonTheme = [];
          var classNameFound = false;

          /**
           * If class is already defined, we add button to class definition
           */
          _this10.options.buttonTheme.map(function (buttonTheme) {
            if (buttonTheme !== null && buttonTheme !== void 0 && buttonTheme["class"].split(" ").includes(classNameItem)) {
              classNameFound = true;
              var buttonThemeArray = buttonTheme.buttons.split(" ");
              if (!buttonThemeArray.includes(button)) {
                classNameFound = true;
                buttonThemeArray.push(button);
                buttonTheme.buttons = buttonThemeArray.join(" ");
              }
            }
            return buttonTheme;
          });

          /**
           * If class is not defined, we create a new entry
           */
          if (!classNameFound) {
            _this10.options.buttonTheme.push({
              "class": classNameItem,
              buttons: buttons
            });
          }
        });
      });
      this.render();
    }

    /**
     * Removes/Amends an entry to the `buttonTheme`. Basically a way to remove a class previously added to a button through buttonTheme or addButtonTheme.
     * @param  {string} buttons List of buttons to select (separated by a space).
     * @param  {string} className Classes to give to the selected buttons (separated by space).
     */
  }, {
    key: "removeButtonTheme",
    value: function removeButtonTheme(buttons, className) {
      var _this11 = this;
      /**
       * When called with empty parameters, remove all button themes
       */
      if (!buttons && !className) {
        this.options.buttonTheme = [];
        this.render();
        return;
      }

      /**
       * If buttons are passed and buttonTheme has items
       */
      if (buttons && Array.isArray(this.options.buttonTheme) && this.options.buttonTheme.length) {
        var buttonArray = buttons.split(" ");
        buttonArray.forEach(function (button) {
          var _this11$options;
          (_this11$options = _this11.options) === null || _this11$options === void 0 || (_this11$options = _this11$options.buttonTheme) === null || _this11$options === void 0 || _this11$options.map(function (buttonTheme, index) {
            /**
             * If className is set, we affect the buttons only for that class
             * Otherwise, we afect all classes
             */
            if (buttonTheme && className && className.includes(buttonTheme["class"]) || !className) {
              var _buttonTheme;
              var filteredButtonArray = (_buttonTheme = buttonTheme) === null || _buttonTheme === void 0 ? void 0 : _buttonTheme.buttons.split(" ").filter(function (item) {
                return item !== button;
              });

              /**
               * If buttons left, return them, otherwise, remove button Theme
               */
              if (buttonTheme && filteredButtonArray !== null && filteredButtonArray !== void 0 && filteredButtonArray.length) {
                buttonTheme.buttons = filteredButtonArray.join(" ");
              } else {
                var _this11$options$butto;
                (_this11$options$butto = _this11.options.buttonTheme) === null || _this11$options$butto === void 0 || _this11$options$butto.splice(index, 1);
                buttonTheme = null;
              }
            }
            return buttonTheme;
          });
        });
        this.render();
      }
    }

    /**
     * Get the DOM Element of a button. If there are several buttons with the same name, an array of the DOM Elements is returned.
     * @param  {string} button The button layout name to select
     */
  }, {
    key: "getButtonElement",
    value: function getButtonElement(button) {
      var output;
      var buttonArr = this.buttonElements[button];
      if (buttonArr) {
        if (buttonArr.length > 1) {
          output = buttonArr;
        } else {
          output = buttonArr[0];
        }
      }
      return output;
    }

    /**
     * This handles the "inputPattern" option
     * by checking if the provided inputPattern passes
     */
  }, {
    key: "inputPatternIsValid",
    value: function inputPatternIsValid(inputVal) {
      var inputPatternRaw = this.options.inputPattern;
      var inputPattern;

      /**
       * Check if input pattern is global or targeted to individual inputs
       */
      if (inputPatternRaw instanceof RegExp) {
        inputPattern = inputPatternRaw;
      } else {
        inputPattern = inputPatternRaw[this.options.inputName || this.defaultName];
      }
      if (inputPattern && inputVal) {
        var didInputMatch = inputPattern.test(inputVal);
        if (this.options.debug) {
          console.log("inputPattern (\"".concat(inputPattern, "\"): ").concat(didInputMatch ? "passed" : "did not pass!"));
        }
        return didInputMatch;
      } else {
        /**
         * inputPattern doesn't seem to be set for the current input, or input is empty. Pass.
         */
        return true;
      }
    }

    /**
     * Handles simple-keyboard event listeners
     */
  }, {
    key: "setEventListeners",
    value: function setEventListeners() {
      /**
       * Only first instance should set the event listeners
       */
      if (this.isFirstKeyboardInstance || !this.allKeyboardInstances) {
        if (this.options.debug) {
          console.log("Caret handling started (".concat(this.keyboardDOMClass, ")"));
        }
        var _this$options$physica = this.options.physicalKeyboardHighlightPreventDefault,
          physicalKeyboardHighlightPreventDefault = _this$options$physica === void 0 ? false : _this$options$physica;

        /**
         * Event Listeners
         */
        document.addEventListener("keyup", this.handleKeyUp, physicalKeyboardHighlightPreventDefault);
        document.addEventListener("keydown", this.handleKeyDown, physicalKeyboardHighlightPreventDefault);
        document.addEventListener("mouseup", this.handleMouseUp);
        document.addEventListener("touchend", this.handleTouchEnd);
        document.addEventListener("selectionchange", this.handleSelectionChange);
        document.addEventListener("select", this.handleSelect);
      }
    }

    /**
     * Event Handler: KeyUp
     */
  }, {
    key: "handleKeyUp",
    value: function handleKeyUp(event) {
      this.caretEventHandler(event);
      if (this.options.physicalKeyboardHighlight) {
        this.physicalKeyboard.handleHighlightKeyUp(event);
      }
    }

    /**
     * Event Handler: KeyDown
     */
  }, {
    key: "handleKeyDown",
    value: function handleKeyDown(event) {
      if (this.options.physicalKeyboardHighlight) {
        this.physicalKeyboard.handleHighlightKeyDown(event);
      }
    }

    /**
     * Event Handler: MouseUp
     */
  }, {
    key: "handleMouseUp",
    value: function handleMouseUp(event) {
      this.caretEventHandler(event);
    }

    /**
     * Event Handler: TouchEnd
     */
    /* istanbul ignore next */
  }, {
    key: "handleTouchEnd",
    value: function handleTouchEnd(event) {
      this.caretEventHandler(event);
    }

    /**
     * Event Handler: Select
     */
    /* istanbul ignore next */
  }, {
    key: "handleSelect",
    value: function handleSelect(event) {
      this.caretEventHandler(event);
    }

    /**
     * Event Handler: SelectionChange
     */
    /* istanbul ignore next */
  }, {
    key: "handleSelectionChange",
    value: function handleSelectionChange(event) {
      /**
       * Firefox is not reporting the correct caret position through this event
       * https://github.com/hodgef/simple-keyboard/issues/1839
       */
      if (navigator.userAgent.includes("Firefox")) {
        return;
      }
      this.caretEventHandler(event);
    }

    /**
     * Called by {@link setEventListeners} when an event that warrants a cursor position update is triggered
     */
  }, {
    key: "caretEventHandler",
    value: function caretEventHandler(event) {
      var _this12 = this;
      var targetTagName;
      if (event.target.tagName) {
        targetTagName = event.target.tagName.toLowerCase();
      }
      this.dispatch(function (instance) {
        var isKeyboard = event.target === instance.keyboardDOM || event.target && instance.keyboardDOM.contains(event.target);

        /**
         * If syncInstanceInputs option is enabled, make isKeyboard match any instance
         * not just the current one
         */
        if (_this12.options.syncInstanceInputs && Array.isArray(event.path)) {
          isKeyboard = event.path.some(function (item) {
            var _item$hasAttribute;
            return item === null || item === void 0 || (_item$hasAttribute = item.hasAttribute) === null || _item$hasAttribute === void 0 ? void 0 : _item$hasAttribute.call(item, "data-skInstance");
          });
        }
        if ((targetTagName === "textarea" || targetTagName === "input" && ["text", "search", "url", "tel", "password"].includes(event.target.type)) && !instance.options.disableCaretPositioning) {
          /**
           * Tracks current cursor position
           * As keys are pressed, text will be added/removed at that position within the input.
           */
          var selectionStart = event.target.selectionStart;
          var selectionEnd = event.target.selectionEnd;
          if (instance.options.rtl) {
            selectionStart = instance.utilities.getRtlOffset(selectionStart, instance.getInput());
            selectionEnd = instance.utilities.getRtlOffset(selectionEnd, instance.getInput());
          }
          instance.setCaretPosition(selectionStart, selectionEnd);

          /**
           * Tracking current input in order to handle caret positioning edge cases
           */
          _this12.activeInputElement = event.target;
          if (instance.options.debug) {
            console.log("Caret at: ", instance.getCaretPosition(), instance.getCaretPositionEnd(), event && event.target.tagName.toLowerCase(), "(".concat(instance.keyboardDOMClass, ")"), event === null || event === void 0 ? void 0 : event.type);
          }
        } else if ((instance.options.disableCaretPositioning || !isKeyboard) && (event === null || event === void 0 ? void 0 : event.type) !== "selectionchange") {
          /**
           * If we toggled off disableCaretPositioning, we must ensure caretPosition doesn't persist once reactivated.
           */
          instance.setCaretPosition(null);

          /**
           * Resetting activeInputElement
           */
          _this12.activeInputElement = null;
          if (instance.options.debug) {
            console.log("Caret position reset due to \"".concat(event === null || event === void 0 ? void 0 : event.type, "\" event"), event);
          }
        }
      });
    }

    /**
     * Execute an operation on each button
     */
  }, {
    key: "recurseButtons",
    value: function recurseButtons(fn) {
      var _this13 = this;
      if (!fn) return;
      Object.keys(this.buttonElements).forEach(function (buttonName) {
        return _this13.buttonElements[buttonName].forEach(fn);
      });
    }

    /**
     * Destroy keyboard listeners and DOM elements
     */
  }, {
    key: "destroy",
    value: function destroy() {
      if (this.options.debug) console.log("Destroying simple-keyboard instance: ".concat(this.currentInstanceName));
      var _this$options$physica2 = this.options.physicalKeyboardHighlightPreventDefault,
        physicalKeyboardHighlightPreventDefault = _this$options$physica2 === void 0 ? false : _this$options$physica2;

      /**
       * Remove document listeners
       */
      document.removeEventListener("keyup", this.handleKeyUp, physicalKeyboardHighlightPreventDefault);
      document.removeEventListener("keydown", this.handleKeyDown, physicalKeyboardHighlightPreventDefault);
      document.removeEventListener("mouseup", this.handleMouseUp);
      document.removeEventListener("touchend", this.handleTouchEnd);
      document.removeEventListener("select", this.handleSelect);
      document.removeEventListener("selectionchange", this.handleSelectionChange);
      document.onpointerup = null;
      document.ontouchend = null;
      document.ontouchcancel = null;
      document.onmouseup = null;

      /**
       * Remove buttons
       */
      var deleteButton = function deleteButton(buttonElement) {
        if (buttonElement) {
          buttonElement.onpointerdown = null;
          buttonElement.onpointerup = null;
          buttonElement.onpointercancel = null;
          buttonElement.ontouchstart = null;
          buttonElement.ontouchend = null;
          buttonElement.ontouchcancel = null;
          buttonElement.onclick = null;
          buttonElement.onmousedown = null;
          buttonElement.onmouseup = null;
          buttonElement.remove();
          buttonElement = null;
        }
      };
      this.recurseButtons(deleteButton);

      /**
       * Remove wrapper events
       */
      this.keyboardDOM.onpointerdown = null;
      this.keyboardDOM.ontouchstart = null;
      this.keyboardDOM.onmousedown = null;

      /**
       * Clearing keyboard rows
       */
      this.resetRows();

      /**
       * Candidate box
       */
      if (this.candidateBox) {
        this.candidateBox.destroy();
        this.candidateBox = null;
      }

      /**
       * Clearing activeInputElement
       */
      this.activeInputElement = null;

      /**
       * Removing instance attribute
       */
      this.keyboardDOM.removeAttribute("data-skInstance");

      /**
       * Clearing keyboardDOM
       */
      this.keyboardDOM.innerHTML = "";

      /**
       * Remove instance
       */
      window["SimpleKeyboardInstances"][this.currentInstanceName] = null;
      delete window["SimpleKeyboardInstances"][this.currentInstanceName];

      /**
       * Reset initialized flag
       */
      this.initialized = false;
    }

    /**
     * Process buttonTheme option
     */
  }, {
    key: "getButtonThemeClasses",
    value: function getButtonThemeClasses(button) {
      var buttonTheme = this.options.buttonTheme;
      var buttonClasses = [];
      if (Array.isArray(buttonTheme)) {
        buttonTheme.forEach(function (themeObj) {
          if (themeObj && themeObj["class"] && typeof themeObj["class"] === "string" && themeObj.buttons && typeof themeObj.buttons === "string") {
            var themeObjClasses = themeObj["class"].split(" ");
            var themeObjButtons = themeObj.buttons.split(" ");
            if (themeObjButtons.includes(button)) {
              buttonClasses = [].concat(Keyboard_toConsumableArray(buttonClasses), Keyboard_toConsumableArray(themeObjClasses));
            }
          } else {
            console.warn("Incorrect \"buttonTheme\". Please check the documentation.", themeObj);
          }
        });
      }
      return buttonClasses;
    }

    /**
     * Process buttonAttributes option
     */
  }, {
    key: "setDOMButtonAttributes",
    value: function setDOMButtonAttributes(button, callback) {
      var buttonAttributes = this.options.buttonAttributes;
      if (Array.isArray(buttonAttributes)) {
        buttonAttributes.forEach(function (attrObj) {
          if (attrObj.attribute && typeof attrObj.attribute === "string" && attrObj.value && typeof attrObj.value === "string" && attrObj.buttons && typeof attrObj.buttons === "string") {
            var attrObjButtons = attrObj.buttons.split(" ");
            if (attrObjButtons.includes(button)) {
              callback(attrObj.attribute, attrObj.value);
            }
          } else {
            console.warn("Incorrect \"buttonAttributes\". Please check the documentation.", attrObj);
          }
        });
      }
    }
  }, {
    key: "onTouchDeviceDetected",
    value: function onTouchDeviceDetected() {
      /**
       * Processing autoTouchEvents
       */
      this.processAutoTouchEvents();

      /**
       * Disabling contextual window on touch devices
       */
      this.disableContextualWindow();
    }

    /**
     * Disabling contextual window for hg-button
     */
    /* istanbul ignore next */
  }, {
    key: "disableContextualWindow",
    value: function disableContextualWindow() {
      window.oncontextmenu = function (event) {
        if (event.target.classList.contains("hg-button")) {
          event.preventDefault();
          event.stopPropagation();
          return false;
        }
      };
    }

    /**
     * Process autoTouchEvents option
     */
  }, {
    key: "processAutoTouchEvents",
    value: function processAutoTouchEvents() {
      if (this.options.autoUseTouchEvents) {
        this.options.useTouchEvents = true;
        if (this.options.debug) {
          console.log("autoUseTouchEvents: Touch device detected, useTouchEvents enabled.");
        }
      }
    }

    /**
     * Executes the callback function once simple-keyboard is rendered for the first time (on initialization).
     */
  }, {
    key: "onInit",
    value: function onInit() {
      if (this.options.debug) {
        console.log("".concat(this.keyboardDOMClass, " Initialized"));
      }

      /**
       * setEventListeners
       */
      this.setEventListeners();
      if (typeof this.options.onInit === "function") this.options.onInit(this);
    }

    /**
     * Executes the callback function before a simple-keyboard render.
     */
  }, {
    key: "beforeFirstRender",
    value: function beforeFirstRender() {
      /**
       * Performing actions when touch device detected
       */
      if (this.utilities.isTouchDevice()) {
        this.onTouchDeviceDetected();
      }
      if (typeof this.options.beforeFirstRender === "function") this.options.beforeFirstRender(this);

      /**
       * Notify about PointerEvents usage
       */
      if (this.isFirstKeyboardInstance && this.utilities.pointerEventsSupported() && !this.options.useTouchEvents && !this.options.useMouseEvents) {
        if (this.options.debug) {
          console.log("Using PointerEvents as it is supported by this browser");
        }
      }

      /**
       * Notify about touch events usage
       */
      if (this.options.useTouchEvents) {
        if (this.options.debug) {
          console.log("useTouchEvents has been enabled. Only touch events will be used.");
        }
      }
    }

    /**
     * Executes the callback function before a simple-keyboard render.
     */
  }, {
    key: "beforeRender",
    value: function beforeRender() {
      if (typeof this.options.beforeRender === "function") this.options.beforeRender(this);
    }

    /**
     * Executes the callback function every time simple-keyboard is rendered (e.g: when you change layouts).
     */
  }, {
    key: "onRender",
    value: function onRender() {
      if (typeof this.options.onRender === "function") this.options.onRender(this);
    }

    /**
     * Executes the callback function once all modules have been loaded
     */
  }, {
    key: "onModulesLoaded",
    value: function onModulesLoaded() {
      if (typeof this.options.onModulesLoaded === "function") this.options.onModulesLoaded(this);
    }
  }, {
    key: "loadModules",
    value:
    /**
     * Load modules
     */
    function loadModules() {
      var _this14 = this;
      if (Array.isArray(this.options.modules)) {
        this.options.modules.forEach(function (KeyboardModule) {
          var keyboardModule = new KeyboardModule(_this14);
          keyboardModule.init && keyboardModule.init(_this14);
        });
        this.keyboardPluginClasses = "modules-loaded";
        this.render();
        this.onModulesLoaded();
      }
    }

    /**
     * Get module prop
     */
  }, {
    key: "getModuleProp",
    value: function getModuleProp(name, prop) {
      if (!this.modules[name]) return false;
      return this.modules[name][prop];
    }

    /**
     * getModulesList
     */
  }, {
    key: "getModulesList",
    value: function getModulesList() {
      return Object.keys(this.modules);
    }

    /**
     * Parse Row DOM containers
     */
  }, {
    key: "parseRowDOMContainers",
    value: function parseRowDOMContainers(rowDOM, rowIndex, containerStartIndexes, containerEndIndexes) {
      var _this15 = this;
      var rowDOMArray = Array.from(rowDOM.children);
      var removedElements = 0;
      if (rowDOMArray.length) {
        containerStartIndexes.forEach(function (startIndex, arrIndex) {
          var endIndex = containerEndIndexes[arrIndex];

          /**
           * If there exists a respective end index
           * if end index comes after start index
           */
          if (!endIndex || !(endIndex > startIndex)) {
            return false;
          }

          /**
           * Updated startIndex, endIndex
           * This is since the removal of buttons to place a single button container
           * results in a modified array size
           */
          var updated_startIndex = startIndex - removedElements;
          var updated_endIndex = endIndex - removedElements;

          /**
           * Create button container
           */
          var containerDOM = document.createElement("div");
          containerDOM.className += "hg-button-container";
          var containerUID = "".concat(_this15.options.layoutName, "-r").concat(rowIndex, "c").concat(arrIndex);
          containerDOM.setAttribute("data-skUID", containerUID);

          /**
           * Taking elements due to be inserted into container
           */
          var containedElements = rowDOMArray.splice(updated_startIndex, updated_endIndex - updated_startIndex + 1);
          removedElements = updated_endIndex - updated_startIndex;

          /**
           * Inserting elements to container
           */
          containedElements.forEach(function (element) {
            return containerDOM.appendChild(element);
          });

          /**
           * Adding container at correct position within rowDOMArray
           */
          rowDOMArray.splice(updated_startIndex, 0, containerDOM);

          /**
           * Clearing old rowDOM children structure
           */
          rowDOM.innerHTML = "";

          /**
           * Appending rowDOM new children list
           */
          rowDOMArray.forEach(function (element) {
            return rowDOM.appendChild(element);
          });
          if (_this15.options.debug) {
            console.log("rowDOMContainer", containedElements, updated_startIndex, updated_endIndex, removedElements + 1);
          }
        });
      }
      return rowDOM;
    }
  }, {
    key: "render",
    value:
    /**
     * Renders rows and buttons as per options
     */
    function render() {
      var _this16 = this;
      /**
       * Clear keyboard
       */
      this.resetRows();

      /**
       * Calling beforeFirstRender
       */
      if (!this.initialized) {
        this.beforeFirstRender();
      }

      /**
       * Calling beforeRender
       */
      this.beforeRender();
      var layoutClass = "hg-layout-".concat(this.options.layoutName);
      var layout = this.options.layout || getDefaultLayout();
      var useTouchEvents = this.options.useTouchEvents || false;
      var useTouchEventsClass = useTouchEvents ? "hg-touch-events" : "";
      var useMouseEvents = this.options.useMouseEvents || false;
      var disableRowButtonContainers = this.options.disableRowButtonContainers;

      /**
       * Adding themeClass, layoutClass to keyboardDOM
       */
      this.keyboardDOM.className = this.getKeyboardClassString(this.options.theme, layoutClass, this.keyboardPluginClasses, useTouchEventsClass);

      /**
       * Adding keyboard identifier
       */
      this.keyboardDOM.setAttribute("data-skInstance", this.currentInstanceName);

      /**
       * Create row wrapper
       */
      this.keyboardRowsDOM = document.createElement("div");
      this.keyboardRowsDOM.className = "hg-rows";

      /**
       * Iterating through each row
       */
      layout[this.options.layoutName || this.defaultName].forEach(function (row, rIndex) {
        var rowArray = row.split(" ");

        /**
         * Enforce excludeFromLayout
         */
        if (_this16.options.excludeFromLayout && _this16.options.excludeFromLayout[_this16.options.layoutName || _this16.defaultName]) {
          rowArray = rowArray.filter(function (buttonName) {
            return _this16.options.excludeFromLayout && !_this16.options.excludeFromLayout[_this16.options.layoutName || _this16.defaultName].includes(buttonName);
          });
        }

        /**
         * Creating empty row
         */
        var rowDOM = document.createElement("div");
        rowDOM.className += "hg-row";

        /**
         * Tracking container indicators in rows
         */
        var containerStartIndexes = [];
        var containerEndIndexes = [];

        /**
         * Iterating through each button in row
         */
        rowArray.forEach(function (button, bIndex) {
          var _buttonDOM$classList;
          /**
           * Check if button has a container indicator
           */
          var buttonHasContainerStart = !disableRowButtonContainers && typeof button === "string" && button.length > 1 && button.indexOf("[") === 0;
          var buttonHasContainerEnd = !disableRowButtonContainers && typeof button === "string" && button.length > 1 && button.indexOf("]") === button.length - 1;

          /**
           * Save container start index, if applicable
           */
          if (buttonHasContainerStart) {
            containerStartIndexes.push(bIndex);

            /**
             * Removing indicator
             */
            button = button.replace(/\[/g, "");
          }
          if (buttonHasContainerEnd) {
            containerEndIndexes.push(bIndex);

            /**
             * Removing indicator
             */
            button = button.replace(/\]/g, "");
          }

          /**
           * Processing button options
           */
          var fctBtnClass = _this16.utilities.getButtonClass(button);
          var buttonDisplayName = _this16.utilities.getButtonDisplayName(button, _this16.options.display, _this16.options.mergeDisplay);

          /**
           * Creating button
           */
          var buttonType = _this16.options.useButtonTag ? "button" : "div";
          var buttonDOM = document.createElement(buttonType);
          buttonDOM.className += "hg-button ".concat(fctBtnClass);

          /**
           * Adding buttonTheme
           */
          (_buttonDOM$classList = buttonDOM.classList).add.apply(_buttonDOM$classList, Keyboard_toConsumableArray(_this16.getButtonThemeClasses(button)));

          /**
           * Adding buttonAttributes
           */
          _this16.setDOMButtonAttributes(button, function (attribute, value) {
            buttonDOM.setAttribute(attribute, value);
          });
          _this16.activeButtonClass = "hg-activeButton";

          /**
           * Handle button click event
           */
          /* istanbul ignore next */
          if (_this16.utilities.pointerEventsSupported() && !useTouchEvents && !useMouseEvents) {
            /**
             * Handle PointerEvents
             */
            buttonDOM.onpointerdown = function (e) {
              _this16.handleButtonClicked(button, e);
              _this16.handleButtonMouseDown(button, e);
            };
            buttonDOM.onpointerup = function (e) {
              _this16.handleButtonMouseUp(button, e);
            };
            buttonDOM.onpointercancel = function (e) {
              _this16.handleButtonMouseUp(button, e);
            };
          } else {
            /**
             * Fallback for browsers not supporting PointerEvents
             */
            if (useTouchEvents) {
              /**
               * Handle touch events
               */
              buttonDOM.ontouchstart = function (e) {
                _this16.handleButtonClicked(button, e);
                _this16.handleButtonMouseDown(button, e);
              };
              buttonDOM.ontouchend = function (e) {
                _this16.handleButtonMouseUp(button, e);
              };
              buttonDOM.ontouchcancel = function (e) {
                _this16.handleButtonMouseUp(button, e);
              };
            } else {
              /**
               * Handle mouse events
               */
              buttonDOM.onclick = function (e) {
                _this16.setMouseHold(false);
                /**
                 * Fire button handler in onclick for compatibility reasons
                 * This fires handler before onKeyReleased, therefore when that option is set we will fire the handler
                 * in onmousedown instead
                 */
                if (typeof _this16.options.onKeyReleased !== "function") {
                  _this16.handleButtonClicked(button, e);
                }
              };
              buttonDOM.onmousedown = function (e) {
                /**
                 * Fire button handler for onKeyReleased use-case
                 */
                if (typeof _this16.options.onKeyReleased === "function" && !_this16.isMouseHold) {
                  _this16.handleButtonClicked(button, e);
                }
                _this16.handleButtonMouseDown(button, e);
              };
              buttonDOM.onmouseup = function (e) {
                _this16.handleButtonMouseUp(button, e);
              };
            }
          }

          /**
           * Adding identifier
           */
          buttonDOM.setAttribute("data-skBtn", button);

          /**
           * Adding unique id
           * Since there's no limit on spawning same buttons, the unique id ensures you can style every button
           */
          var buttonUID = "".concat(_this16.options.layoutName, "-r").concat(rIndex, "b").concat(bIndex);
          buttonDOM.setAttribute("data-skBtnUID", buttonUID);

          /**
           * Adding button label to button
           */
          var buttonSpanDOM = document.createElement("span");
          buttonSpanDOM.innerHTML = buttonDisplayName;
          buttonDOM.appendChild(buttonSpanDOM);

          /**
           * Adding to buttonElements
           */
          if (!_this16.buttonElements[button]) _this16.buttonElements[button] = [];
          _this16.buttonElements[button].push(buttonDOM);

          /**
           * Appending button to row
           */
          rowDOM.appendChild(buttonDOM);
        });

        /**
         * Parse containers in row
         */
        rowDOM = _this16.parseRowDOMContainers(rowDOM, rIndex, containerStartIndexes, containerEndIndexes);

        /**
         * Appending row to hg-rows
         */
        _this16.keyboardRowsDOM.appendChild(rowDOM);
      });

      /**
       * Appending row to keyboard
       */
      this.keyboardDOM.appendChild(this.keyboardRowsDOM);

      /**
       * Calling onRender
       */
      this.onRender();
      if (!this.initialized) {
        /**
         * Ensures that onInit and beforeFirstRender are only called once per instantiation
         */
        this.initialized = true;

        /**
         * Handling parent events
         */
        /* istanbul ignore next */
        if (this.utilities.pointerEventsSupported() && !useTouchEvents && !useMouseEvents) {
          document.onpointerup = function (e) {
            return _this16.handleButtonMouseUp(undefined, e);
          };
          this.keyboardDOM.onpointerdown = function (e) {
            return _this16.handleKeyboardContainerMouseDown(e);
          };
        } else if (useTouchEvents) {
          /**
           * Handling ontouchend, ontouchcancel
           */
          document.ontouchend = function (e) {
            return _this16.handleButtonMouseUp(undefined, e);
          };
          document.ontouchcancel = function (e) {
            return _this16.handleButtonMouseUp(undefined, e);
          };
          this.keyboardDOM.ontouchstart = function (e) {
            return _this16.handleKeyboardContainerMouseDown(e);
          };
        } else if (!useTouchEvents) {
          /**
           * Handling mouseup
           */
          document.onmouseup = function (e) {
            return _this16.handleButtonMouseUp(undefined, e);
          };
          this.keyboardDOM.onmousedown = function (e) {
            return _this16.handleKeyboardContainerMouseDown(e);
          };
        }

        /**
         * Calling onInit
         */
        this.onInit();
      }
    }
  }]);
  return SimpleKeyboard;
}();
/* harmony default export */ const Keyboard = (SimpleKeyboard);
;// CONCATENATED MODULE: ./src/lib/index.modern.ts


/* harmony default export */ const index_modern = (Keyboard);
})();

SimpleKeyboard = __webpack_exports__;
/******/ })()
;
//# sourceMappingURL=index.modern.js.map