#show spacecats test plugin
# Adapted from work by LanceMaverick
import logging
import telepot
import telepot.aio
from skybeard.beards import BeardChatHandler
from skybeard.predicates import regex_predicate
from skybeard.decorators import onerror
from skybeard.utils import get_args
from . import TelePlot as tp
import os
import equatic
class TelePlotSB(BeardChatHandler):
    __userhelp__ = """
    Makes plots with the /teleplot command. e.g: /teleplot x**2

    Additional options can be parsed to the command:


    Title:
    
    <code>-title "This Title Has Some $LaTeX$"</code>

    Axis Labelling: 
    
    <code>-xlabel "label with $someLaTeX$"</code>
    <code>-ylabel "label"</code>

    Plot Range: 
    
    <code>-range [0,10,100]</code>
    <code>-range [0,10]</code>

    LineStyle (<code>[--]dashed</code>/<code>[:]dotted</code>/<code>[.-]dotdash</code>/<code>none</code>): 
    
    <code>-linestyle .-</code>
    <code>-linestyle dashdot</code>

    Color(<code>[r]red</code>/<code>[g]green</code>/<code>[c]cyan</code>/<code>[k]black</code>/<code>[w]white</code>/<code>[m]magenta</code>): 

    <code>-color red</code>
    <code>-color r</code>

    MarkerStyle (<code>[.]point</code>/<code>[,]pixel</code>/<code>[o]circle</code>/<code>[v]dtriangle</code>/<code>[^]triangle</code>/ 
                 <code>[&lt;]ltriangle</code>/<code>[>]rtriangle</code>/<code>[8]octagon</code>/<code>[s]square</code>/<code>[p]pentagon</code>/ 
                 <code>[*]star</code>/<code>[h]hexagon</code>/<code>[+]plus</code>/<code>[D]diamond</code>/<code>[d]diamond2</code>/ 
                 <code>[|]vline</code>/<code>[_]hline</code>/<code>tickleft</code>/<code>tickright</code>/<code>tickup</code>/<code>tickdown</code>/ 
                 <code>caretleft</code>/<code>caretright</code>/<code>caretup</code>/<code>caretdown</code>):
 
    <code>-markerstyle *</code> 
    <code>-markerstyle star</code> 

    
     """

    __commands__ = [
        ("teleplot", "makePlot", "make a plot." ),
    ]

    @onerror
    async def makePlot(self, msg):
        logger = logging.getLogger("TelePlot")
        logger.setLevel(logging.DEBUG)
        logging.basicConfig()
        in_args = get_args(msg['text']) 
        logger.debug("Got arguments: %s", in_args)
        options = []
         
        for element in in_args:
            if element in ['-xlabel', '-ylabel', '-range', '-marker', '-linestyle', '-options', '-color', '-title']:
                logger.debug("Found option '%s'", element)
                arg_index = in_args.index(element)
                logger.debug("Adding option (%s, %s)", element, in_args[arg_index+1])
                options.append((element, in_args[arg_index+1]))

        try:
            plotter = tp.TelePlot(in_args[0], options, debug='ERROR')
            try:
                file_name = plotter.save_plot()
                await self.sender.sendPhoto(('temp.png', open('{}'.format(file_name), 'rb')))
                os.remove('{}'.format(file_name))
            except SystemExit:
                logger.error("Invalid User Input")
                await self.sender.sendMessage("Ooops! I did not understand your request.")
        except SyntaxError:
            logger.error("Invalid User Options")
            await self.sender.sendMessage("The Plot Options You Have Specified Are Not Valid.")
