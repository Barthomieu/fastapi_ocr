import cv2

def preprocess_image(image_path):
	print(image_path)
	# load the input image and convert it to grayscale
	image = cv2.imread(image_path)

	#convert to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# threshold the image using Otsu's thresholding method
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	# apply median blurring to remove any blurring
	gray = cv2.medianBlur(gray, 3)

	# save the processed image in the /static/uploads directory
	#ofilename = os.path.join(app.config['UPLOAD_FOLDER'], "{}.png".format(os.getpid()))
	cv2.imwrite(image_path, gray)

	return image_path