const WIDTH = window.innerWidth / 2
const HEIGHT = window.innerHeight / 2

var progress = 0
var slideShow = []

var images = []
var imageIndex = 0
var zoomIndex = 1
var dinabug
var externImgClone, internImgClone

var newWidth = WIDTH, newHeight = HEIGHT, x = 0, y = 0

var insideWidth = WIDTH * 0.1, insideHeight = HEIGHT * 0.1
var loading = true

function preload() {
  images = [
    loadImage('assets/1_base.png'),
    loadImage('assets/2_base.png'),
    loadImage('assets/3_base.png')
  ]
  dinabug = loadImage('assets/dinabug.png')
  
}

const sleep = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms))
}

const blend = (currentImage, nextImage, blended) => {
  for(let i = 1; i <= 10; i = i * 1.2) {
      progress = i

      newWidth = WIDTH * i
      newHeight = HEIGHT * i
      
      // Aplicando zoom
      externImgClone = currentImage.get() 
      externImgClone.resize(newWidth, newHeight)

      // Index do crop
      x = (newWidth - WIDTH) / 2
      y = (newHeight - HEIGHT) / 2


      insideWidth = WIDTH * 0.1 * i
      insideHeight = HEIGHT * 0.1 * i

      internImgClone = nextImage.get()
      internImgClone.resize(insideWidth, insideHeight)

      blended.push({
        extern: {
          image: externImgClone,
          1: 0,
          2: 0,
          3: WIDTH,
          4: HEIGHT,
          5: x,
          6: y,
          7: WIDTH,
          8: HEIGHT
        },

        intern: {
          image: internImgClone,
          1: (WIDTH/2) - (insideWidth/2),
          2: (HEIGHT/2) - (insideHeight/2),
          3: insideWidth,
          4: insideHeight,
          5: 0,
          6: 0,
          7: insideWidth,
          8: insideHeight

        }
      })
      // setTimeout(() => {blend(currentImage, nextImage, blended)}, 1)
  }

  return blended
}

const createAnimation = () => {
  let blendToPush = []
  let parameterArray = []
  for(let i = 0; i < images.length; i ++) {
    
    if (i == images.length - 1)
      blendToPush = blend(images[i].get(), images[0].get(), parameterArray)
    else
      blendToPush = blend(images[i].get(), images[i+1].get(), parameterArray)

    slideShow = slideShow.concat(blendToPush)
  }
  loading = false
}

function setup() {
  createCanvas(WIDTH, HEIGHT);

  for(let i of images) {
    i.resize(WIDTH, HEIGHT)
  }
  createAnimation()
}

var printed = false

function draw() {
  if (loading)
    text('Carregando...', 0, 0)
  else {
    let current = slideShow[zoomIndex]
    printed = true
    let e = current.extern
    let i = current.intern

    image(e.image, e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8])
    image(i.image, i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
  }
}

function keyPressed() {
  if (keyCode == UP_ARROW) {
    if (zoomIndex == slideShow.length - 1)
      zoomIndex = 0
    else
      zoomIndex ++
  } else if (keyCode == DOWN_ARROW) {
      if (zoomIndex == 0)
        zoomIndex = slideShow.length - 1
      else
        zoomIndex --
  }
  imageIndex = imageIndex % images.length
}