#-----------------------------------------------------------------------------#
#                                                                             #
# This is a script which is designed to apply masks that were created from    #
# the Stokes Q and U, and polarisation gradient sources, and apply these      #
# masks to the Stokes Q and U maps.                                           #
#                                                                             #
# Author: Chris Herron                                                        #
# Start Date: 4/11/2015                                                       #
#                                                                             #
#-----------------------------------------------------------------------------#

# Import the various packages which are required for the proper functioning of
# this script
import numpy as np
from astropy.io import fits

# Define the apply_mask function, which will mask the Stokes Q and U images, 
# and save the result
def apply_mask(input_image, mask_loc, save_filename):
	'''
	Description
        This function takes an image, and applies the given mask to it, so that
        pixels with a True value in the mask are set to NaN in the image. The 
        produced masked image is saved using the given filename.
        
    Required Input
        input_image - The image to be masked. This should be a string giving 
        			  the directory and filename of the FITS image to be masked.
        mask_loc - The mask to be applied to the image. This should be a string 
        	   giving the directory and filename of the FITS image to be used
        	   as a mask. This image should only have True/False, or 1/0
        	   values throughout.
        save_filename - The filename to save the masked image to. Should be a 
        				string.
                   
    Output
        The masked image is saved to the given filename. Returns 1 if the 
        function runs to completion.
	'''

	# Open the given image, and extract its data
	hdulist = fits.open(input_image)
	data = hdulist[0].data

	# Open the mask, and extract its data
	mask_hdulist = fits.open(mask_loc)
	mask = mask_hdulist[0].data

	# Make sure that the data contains floats (needed to prevent ValueError
	# when assigning NaNs)
	data = data.astype(np.float)
	# Set any pixels that fall inside the mask to be NaN
	data[mask == 1] = np.nan
	# Set the data attribute of the FITS file to the new masked image
	hdulist[0].data = data
	# Save the masked image using the given filename
	hdulist.writeto(save_filename, clobber=True)

	# Print a message saying that the file saved correctly
	print '{} saved successfully'.format(save_filename)

	# Since the file saved correctly, return 1
	return 1

# Set the flux threshold to use to create the first mask, expressed as a
# fraction of the peak flux of the source
thresh1 = 0.05

# Create a string object which stores the directory of the CGPS data
data_loc = '/Users/chrisherron/Documents/PhD/CGPS_2015/'

# Create a string that will be used to control what Q and U FITS files are used
# to perform calculations, and that will be appended into the filename of 
# anything produced in this script. This is either 'high_lat' or 'plane'
mosaic_area = 'plane'

# Create a string that stores the location of the Stokes Q image
Sto_Q_file = data_loc + 'Sto_Q_' + mosaic_area + '.fits'

# Create a string that stores the location of the Stokes U image
Sto_U_file = data_loc + 'Sto_U_' + mosaic_area + '.fits'

# Create a string that stores the location of the mask to use 
mask_file = data_loc + 'combined_mask_{}_thr_{}.fits'.format(mosaic_area, thresh1)

# Create a string that stores the filename to which to save the masked 
# Stokes Q file 
save_Q_file = data_loc + 'Sto_Q_' + mosaic_area + '_final_mask.fits'

# Create a string that stores the filename to which to save the masked 
# Stokes U file 
save_U_file = data_loc + 'Sto_U_' + mosaic_area + '_final_mask.fits'

# Run the apply_mask function, to apply the mask to the Stokes Q image, and
# save the produced image as a FITS file.
apply_mask(Sto_Q_file, mask_file, save_Q_file)

# Run the apply_mask function, to apply the mask to the Stokes U image, and
# save the produced image as a FITS file.
apply_mask(Sto_U_file, mask_file, save_U_file)

# Print a message to say that everything has been masked successfully
print 'All images masked successfully'