#!/usr/bin/perl

use warnings;
use strict;

#use patterns;

## Bevor die Praeambel ausgegeben wird, wird der Notenschluessel abhängig vom verwendeten Notenumfang berechnet.
## Und dafür werden erstmal die Noten definiert. Hier oben sind sie auch leichter zu finden. Praktisch.
my @intervalle = qw(Prim Sek Terz Quart Quint Sext Sep Okt);
my $maximal_intervall = 1; # wird aber um zwei addiert, da nachfolgende Intervalle kleiner sein sollen. Also ist 2 eigentich eine Quint.
my @noten = qw(e2 e2 f2 a2 b2 c3 d3 e3 f3 g3 a3 b3 c4 d4); # g2 entfernt
my $tonart = 'D-Dur';
my @pause_oder_note = qw(note note);
my $notenumfang = @noten;
my $notenindex = int(rand($notenumfang)); # Das ist die erste Note. Nach ihr richtet sich der Notenschluessel.

## Hier fängt die Definition der Praeambelelemente an.
## Zwölf Zahlen stehen als erstes in der Praeambel, durch whitespace getrennt.
## Die ersten acht beschreiben musikalische Daten.
my $anzahl_notensysteme = 1;		# Anzahl der Notensysteme (relativ zu der Anzahl der Instrumente)
my $anzahl_instrumente = 1;		# Anzahl der Instrumente
my $logischer_metrumzaehler = 4;	# Logischer Metrumzähler
my $logischer_metrumnenner = 4;		# Logischer Metrumnenner
my $gedruckter_metrumzaehler = 4;	# Gedruckterer Metrumzähler
my $gedruckter_metrumnenner = 4;	# Gedruckterer Metrumnenner
my $auftaktschlaege = 0;		# Anzahl logischer Schläge im ersten Auftakt. Dezimalbrüche sind möglich.
my $anzahl_vorzeichen = 0;		# Vorzeichen entsprechend dem Quintenzirkel. Positive Zahlen sind Kreuze, negative sind bs.

## Die naechsten vier beschreiben drucktechnische Details.
my $anzahl_seiten = 2;			# Anzahl der Seiten, die das Dokument haben soll
my $anzahl_systeme = 26;		# Anzahl der Notensysteme, d.h. gedruckter Partiturzeilen
my $groesse_system = 16;		# Größe eines Notensystems in pt
my $einrueckung = .1;			# Einrückung in Prozent. 8.5 % schreibt man als .085

## Namen der Instrumente, von unten nach oben.
my $instrumentenbezeichnung = "Bass"; # Wird vor das jeweilige Notensystem geschrieben. Kann leergelassen werden.

## Titel des Stücks. Wird zusammengestellt aus den Intervallen und dem
# Notenumfang.

my $titel = "Tt\nZufallssequenzen in Sek-".$intervalle[$maximal_intervall+2]." aus ".$noten[1].' - '.$noten[$#noten].' ohne g2';

## Notenschlüssel, von unten nach oben.
# b heißt Bassschlüssel, t heißt Violinschlüssel. Wird in &notenschluessel berechnet.
#my $notenschluessel = &notenschluessel(); # eigentlich
my $notenschluessel = 'b';

## Das Verzeichnis, in das die Tex-Datei geschrieben werden soll.
my $verzeichnis = "./\n"; # ./

sub praeambel {
	print "\% PRAEAMBEL\n";
	print $anzahl_notensysteme;
	print " ";
	print $anzahl_instrumente;
	print " ";
	print $logischer_metrumzaehler;
	print " ";
	print $logischer_metrumnenner;
	print " ";
	print $gedruckter_metrumzaehler;
	print " ";
	print $gedruckter_metrumnenner;
	print " ";
	print $auftaktschlaege;
	print " ";
	print $anzahl_vorzeichen;
	print "\n";
	print $anzahl_seiten;
	print " ";
	print $anzahl_systeme;
	print " ";
	print $groesse_system;
	print " ";
	print $einrueckung;
	print "\n";
	print $instrumentenbezeichnung;
	print "\n";
	print $notenschluessel;
	print "\n";
	print $verzeichnis;
	print "\n";
	print $titel;
	print "\n";
}

my @dauern = qw(6 3 1 8 4 2 0);

if ($tonart eq 'C-Dur' || $tonart eq 'a-Moll') {
	$anzahl_vorzeichen = 0;
}
elsif ($tonart eq 'G-Dur' || $tonart eq 'e-Moll') {
	$anzahl_vorzeichen = 1;
}
elsif ($tonart eq 'D-Dur' || $tonart eq 'b-Moll') {
	$anzahl_vorzeichen = 2;
}
elsif ($tonart eq 'A-Dur' || $tonart eq 'fis-Moll') {
	$anzahl_vorzeichen = 3;
}
elsif ($tonart eq 'E-Dur' || $tonart eq 'cis-Moll') {
	$anzahl_vorzeichen = 4;
}
elsif ($tonart eq 'B-Dur' || $tonart eq 'gis-Moll') {
	$anzahl_vorzeichen = 5;
}

## Gib die Präambel aus
&praeambel();

## Gib den Korpus aus
&corpus();

sub corpus {
	# Notennamen werden immer klein geschrieben. Dahinter eine Ziffer für die Länge(0,2,4,8,1,3,6)
	# und eine Ziffer für die Oktave(c' hat die Ziffer 4, C hat die Ziffer 3)
	# s steht für sharp(#) und f steht für flat(b). Ganze Note Cis schreibt man also cs03
	print "\% CORPUS\n";
#	&pattern442_4444_442();
#	&simple_pattern();

# Gibt die Seitennummer (P = Pagenumber) aus. r = Right. c = Text.
# I ist Anweisung für midi. i ist Instrument, 34 ist mit Plektrum gezupfter Bass.
# K-8-0 ist die Anweisung zum herunteroktavieren. Dabei werden die Noten um eine Oktave tiefer ausgegeben.
# T-12 ist die Anweisung zum Transponieren um 12 Halbtöne nach unten beim Schreiben der Midi-Datei.
print "Prc Ii34T-12 ";
	&complex_pattern();
	
}



sub complex_pattern {
  # $bloeder_zaehler iteriert über @intervall_muster. Er wird auf 0 zurückgesetzt, wenn das letzte Element im array ausgegeben wurde.
  my $bloeder_zaehler = 0;
	my $string;
	my @hoch_oder_runter = qw(+ -);
	my $richtung;
	my $vormals_richtung;
	my $vor_vormals_richtung;
	
	my $aktuelle_note = $noten[$notenindex];
	my $schritte;
	
	for (1..$anzahl_systeme) {
	  my $erstes_intervall = int(rand($maximal_intervall))+2;
	  my $zweites_intervall = int(rand($erstes_intervall));
	     $zweites_intervall++ if $zweites_intervall == 0;
	  my $drittes_intervall = 1-$erstes_intervall;
#	     $drittes_intervall++ if $drittes_intervall == 0;
	  my @intervall_muster = ('dummy', $erstes_intervall, $zweites_intervall, $drittes_intervall);
		for (1..3) { # erster, zweiter, dritter takt
			my $taktaufloesung = 8;
			my $verbleibende_taktdauer = 1;
			my $interne_maximaltaktdauer;

			$interne_maximaltaktdauer = 7 if $taktaufloesung == 64;
			$interne_maximaltaktdauer = 6 if $taktaufloesung == 32;
			$interne_maximaltaktdauer = 5 if $taktaufloesung == 16;
			$interne_maximaltaktdauer = 4 if $taktaufloesung == 8;
			$interne_maximaltaktdauer = 3 if $taktaufloesung == 4;
			$interne_maximaltaktdauer = 2 if $taktaufloesung == 2;
			$interne_maximaltaktdauer = 1 if $taktaufloesung == 1;

			my $interne_maximaltaktdauer_fix = $interne_maximaltaktdauer;
			my @interne_dauern = qw(0 2 4 8 1 3 6);
			my @normale_dauern = qw(1 2 4 8 16 32 64);
			
			my $schwellenwert = 1-(1/$taktaufloesung);
			my $aktuelle_notendauer;
			my $aktuelle_notendauer_normal;
			while($verbleibende_taktdauer >= (1/$taktaufloesung)) {
				my $zufallszahl = 8;
				$aktuelle_notendauer = $interne_dauern[($interne_maximaltaktdauer_fix-$zufallszahl)];
				$aktuelle_notendauer_normal = $normale_dauern[($interne_maximaltaktdauer_fix-$zufallszahl)];
				$verbleibende_taktdauer -= (1/$aktuelle_notendauer_normal);

				if ($verbleibende_taktdauer <= $schwellenwert) {
					$schwellenwert = $schwellenwert-((1-$schwellenwert));
					$interne_maximaltaktdauer--;
				}
				
				$aktuelle_note = $noten[$notenindex];
        $bloeder_zaehler++;
        die "bloeder zaehler ist null" if $bloeder_zaehler == 0;
        $schritte = $intervall_muster[$bloeder_zaehler];
        $bloeder_zaehler = 0 if $bloeder_zaehler == $#intervall_muster;
        
				# Die folgenden zwei if-Verzweigungen regeln die Richtungsänderung bei
				# Erreichen der Notenumfanggrenze.
				if (($notenindex < ($schritte+1) && $hoch_oder_runter[$richtung] eq '-')) {
					$richtung = 0;
					$vormals_richtung = $richtung;
				}
				if (($notenindex > $notenumfang-($schritte+1) && $hoch_oder_runter[$richtung] eq '+')) {
					$richtung = 1;
					$vormals_richtung = $richtung;
				}
				$notenindex += $schritte if $hoch_oder_runter[$richtung] eq '+';
				$notenindex -= $schritte if $hoch_oder_runter[$richtung] eq '-';
				$aktuelle_note = $noten[$notenindex];
				$aktuelle_note =~ s/(.)$/$aktuelle_notendauer$1/;
				$string .= $aktuelle_note." ";
			}
			$string .= " /\n";
		}
	}
	print $string;
}

sub notenschluessel {
	my $notenschluessel;
	print "\% index: $notenindex, note: $noten[$notenindex]\n";
	$notenschluessel = 't' if $noten[$notenindex] =~ /[45]$/;
	$notenschluessel = 'b' if $noten[$notenindex] =~ /[23]$/;
	return $notenschluessel;
}






