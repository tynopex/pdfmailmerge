from PyPDF2             import PdfFileReader, PdfFileWriter
from PyPDF2.generic     import NameObject, StreamObject
from PyPDF2.generic     import ArrayObject, DictionaryObject


def mailmerge( ifile, ofile, fn_updatetmpl, content_list ):

    with open( ifile, "rb" ) as f:
        pdf = PdfFileReader( f )
        out = PdfFileWriter( )

        # Get and update template page
        pg = pdf.getPage( 0 )
        if fn_updatetmpl:
            fn_updatetmpl( pg )

        # Use one copy of template contents and page resources dictionary
        tmpl = out._addObject( pg.getContents() )
        res  = out._addObject( pg['/Resources'] )

        # Generate page for each content element
        for cdata in content_list:
            d = { '/Length' : len(cdata), '__streamdata__' : cdata }
            c = StreamObject.initializeFromDictionary( d )

            p = DictionaryObject( pg.items() )
            p[NameObject('/Contents')] = ArrayObject( [tmpl,c] )
            out.addPage( p )

        # Write complete output file
        with open( ofile, "wb" ) as g:
            out.write( g )


def test_pageno():

    # Writes page number near bottom
    tmpl = "BT /F1 12 Tf 18 TL 72 18 Td (Page {}) Tj ET"
    content = [ tmpl.format(i) for i in range( 1000 ) ]

    def update_pg( pg ):
        res = pg[NameObject('/Resources')]

        # Add font
        res[NameObject("/Font")] = DictionaryObject( {
            NameObject("/F1") : DictionaryObject( {
                NameObject("/Type")     : NameObject("/Font"),
                NameObject("/Subtype")  : NameObject("/Type1"),
                NameObject("/BaseFont") : NameObject("/Helvetica"),
                } ),
            } )

        # Ensure /Text is in /ProcSet
        if NameObject('/Text') not in res[NameObject('/ProcSet')]:
            res[NameObject("/ProcSet")].append( NameObject("/Text") )

    mailmerge( "sample.pdf", "out.pdf", update_pg, content )
