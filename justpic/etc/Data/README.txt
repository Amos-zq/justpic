
   This directory contains the data used for the ECCV 2002 paper, "Object
   Recognition as Machine Translation", by Pinar Duygulu, Kobus Barnard, Nando
   do Freitas, and David Forsyth. The data is very much cobbled together and has
   some anomalies. More carefully prepared data will be made available in the
   future. 

   Each image segment is represented by 36 features. Since each image has a
   different number of segments, we list the number of segments used in
   separate files, so that the entire set of image segments can be read into a
   single Matlab file.  
   
   To compute the color features the images were linearized on the basis that
   they were PCD images, and then for convenience they were scaled up by
   (255/107), a somewhat arbitrary factor which has some justification based on
   the PCD format. (In hindsight, a factor of 2 would make more sense, but using
   this, or any other factor, would not change anything). Note that the features
   are redundant. Note also that the RGB and L*a*b features were duplicated to
   increase their weight for a specific experiment (long since finished), and we
   did not subsequently remove the duplicated duplicated columns. I do not know
   if this duplication inadvertently helps, hinders, or has no effect on the
   ECCV experiments. However, if you need a non-singular feature matrix, you
   will have to remove them. The 36 features are: 

        area, x, y, boundary/area, convexity, moment-of-inertia  (6)
        ave RGB (3)
        ave RGB (3, yes, duplicated!)
        RGB stdev (3)
        ave L*a*b (3)
        ave L*a*b (3, yes, duplicated!)
        lab stdev (3)
        mean oriented energy, 30 degree increments   (12)


   The files are as follows. 

        words
           The vocabulary used. We count the words starting at 1, so "city" is
           word 1. 

        blob_counts
        test_1_blob_counts
           One number per line for the 4500 training / 500 test_1 images,
           giving the number of blobs used for that image. 

        blobs
        test_1_blobs
           The features for the blobs for the 4500 training / 500 test_1
           images, listed in order of images, then decreasing blob size. In
           order to tell which blob goes with which image, you need either the
           file blob_counts, or the file document_blobs. 

        document_blobs
        test_1_document_blobs
           (EDITED april 4, 2004: The original writing suggested
           that these files supplied the blob tokens. However, these files
           simply point to the actual blobs. To get the tokens that were used
           for the ECCV 2002 paper, consult the files cluster_membership and
           test_1_cluster_membership.)

           The blob for each of the 4500 training / 500 test_1 images.  Each
           line has a list of numbers representing indicies into the file
           "blobs". If the image has fewer blobs than the maximum, the row is
           padded with -99's so that the file can be read as a Matlab matrix.

           (The names of these files are somewhat misleading because they are
           not exactly analogous with the files document_words and
           test_1_document_words.  These files do not give you any more
           information than what is available in blob_counts and
           test_1_blob_counts.)

        cluster_membership
        test_1_cluster_membership
           The blob token associated with each line of the file blobs and
           test_1_blobs. 

        document_words
        test_1_document_words
           The words for each of the 4500 training / 500 test_1 images. Each
           line has a list of numbers which are indicies into the vocabulary
           file "words".  Counting starts at 1. If the image has fewer blobs
           than the maximum, the row is padded with -99's so that the file can
           be read as a Matlab matrix. 

        word_counts
        test_1_word_counts
           The number of words for each of the 4500 training / 500 test_1
           images.  

        image_nums
        test_1_image_nums
           The Corel image number for the 4500 training / 500 test_1 images.
           We are unable to distribute the actual images due to copyright
           restrictions.  The data can be used with some extent without the
           images. We provide the image numbers for those who have access to
           the Corel images. 
           

    Segmentation masks.

        The directory seg_masks contains files of the form
        m_<corel_num>_region_map.mat.gz

        These files are Matlab integer matrices which give the region number for
        each pixel in the image. We use 0 for unassigned. Since the segmentation
        software we used stripped the outer 10 pixels for each image, these are
        always 0. 

        IMPORTANT NOTE: The order of the regions is arbitrary. In the data sets,
        the regions are ordered by size. In the segmentation masks, the regions
        are in arbitrary order. There may be more regions in the segmentation
        masks, because we only used the 10 largest regions for the data. The
        main purpose of the masks is so that those who have the images can use
        the same regions but different features. (Since we used very simple
        features, and ignored the surrounding regions, we are confident that
        there is much scope for improvement in these directions.) 

